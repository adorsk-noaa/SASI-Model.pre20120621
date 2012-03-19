# Populates table of habitat_types from shapefile
# Assumes that substrates and features have already been populated.
import sasi.conf.conf as conf
import sasi.conf.feature_assignments as feature_assignments
import sasi.conf.substrate_mappings as substrate_mappings
import sasi.conf.energy_mappings as energy_mappings

from sasi.habitat.habitat_type import Habitat_Type
from sasi.habitat.habitat import Habitat
from sasi.habitat.substrate import Substrate
from sasi.habitat.feature import Feature

import sasi.sa.session as sa_session
import sasi.sa.habitat.habitat as sa_habitat
import sasi.sa.habitat.habitat_type as sa_habitat_type
import sasi.sa.habitat.cell as sa_cell
import sasi.sa.habitat.feature as sa_feature
import sasi.sa.habitat.substrate as sa_substrate

import ogr
from shapely import wkb
from shapely.geometry import Polygon, MultiPolygon

from sqlalchemy import func, MetaData
from geoalchemy.functions import functions as geo_func
from geoalchemy.geometry import Geometry

import sys

def main():


	# Get db session.
	session = sa_session.get_session()

	# Clear habitat_type tables
	for t in [sa_habitat.table]:
		session.execute(t.delete())

	# Load shapefile
	sf = ogr.Open(conf.conf['sasi_habitat_file'])
	
	# Get feature layer.
	layer = sf.GetLayer(0)

	# Get layer srs.
	layer_srs = layer.GetSpatialRef()

	# Set target srs to 4326 (default used by most GIS software).
	target_srs = ogr.osr.SpatialReference()
	target_srs.ImportFromEPSG(4326)

	# Get fields.
	layer_def = layer.GetLayerDefn()
	field_count = layer_def.GetFieldCount()
	fields = [layer_def.GetFieldDefn(i).GetName() for i in range(field_count)]

	# Initialize a list to hold habitat objects.
	habitats = []

	# For each cell feature... 
	counter = 0
	features = [f for f in layer]
	for f in features:

		if (counter % 1000) == 0: print >> sys.stderr, "%s" % (counter),
		counter += 1

		# Get feature attributes.
		f_attributes = {}
		for i in range(field_count): 
			f_attributes[fields[i]] = f.GetField(i)

		# Skip blank rows.
		if (not f_attributes['SOURCE']): continue

		# Get feature geometry. 
		ogr_g = f.GetGeometryRef()

		# Transform to target_srs.
		ogr_g = f.GetGeometryRef()
		ogr_g.TransformTo(target_srs)

		# We convert each feature into a multipolygon, since
		# we may have a mix of normal polygons and multipolygons.
		geom = wkb.loads(ogr_g.ExportToWkb())
		if geom.geom_type =='Polygon':
			geom = MultiPolygon([(geom.exterior.coords, geom.interiors )])

		# Get habitat_type's energy code.
		energy = energy_mappings.shp_to_va[f_attributes['Energy']] 
		
		# Get habitat_type's substrate object.
		substrate_id = substrate_mappings.shp_to_va[f_attributes['TYPE_SUB'].strip()]
		substrate = session.query(Substrate).filter(Substrate.id == substrate_id).one()

		# Get habitat_type object.
		habitat_type = session.query(Habitat_Type).join(Habitat_Type.substrate).filter(Substrate.id == substrate_id).filter(Habitat_Type.energy == energy).one()

		# Make habitat object from feature data.
		r = Habitat(
				id_km100 = f_attributes['100km_Id'],
				id_km1000 = f_attributes['1000Km_Id'],
				id_vor = f_attributes['Vor_id'],
				z = f_attributes['z'],
				habitat_type = habitat_type,
				area = f_attributes['Area_Km'],	
				geom = geom.wkt
				)

		habitats.append(r)	

	
	print >> sys.stderr, "Writing habitats to db"
	session.add_all(habitats)
	session.commit()

	print >> sys.stderr, "Calculating areas for habitats."
	habitat_area = geo_func.area(func.geography(Habitat.geom)).label('habitat_area')
	habitat_infos = session.query(Habitat, habitat_area).all()
	for (habitat, habitat_area) in habitat_infos:
		habitat.area = habitat_area
	session.commit()

	print >> sys.stderr, "done"

if __name__ == '__main__':
	main()
