# Populates table of habitats from shapefile
# Assumes that substrates and features have already been populated.
import sasi.conf.conf as conf
import sasi.conf.feature_assignments as feature_assignments
import sasi.conf.substrate_mappings as substrate_mappings
import sasi.conf.energy_mappings as energy_mappings

from sasi.habitat.habitat import Habitat
from sasi.habitat.substrate import Substrate
from sasi.habitat.feature import Feature

import sasi.sa.session as sa_session
import sasi.sa.habitat.habitat as sa_habitat
import sasi.sa.habitat.cell as sa_cell
import sasi.sa.habitat.feature as sa_feature
import sasi.sa.habitat.substrate as sa_substrate

import ogr
from shapely import wkb
from shapely.geometry import Polygon, MultiPolygon

from sqlalchemy import func, MetaData
from geoalchemy.functions import functions as geo_func
from geoalchemy.geometry import Geometry

def main():


	# Get db session.
	session = sa_session.get_session()

	# Clear habitat tables
	for t in [sa_habitat.habitats_features_table, sa_habitat.habitat_table]: 
		session.execute(t.delete())
	session.commit()

	# Load shapefile
	sf = ogr.Open(conf.conf['sasi_habitat_file'])
	
	# Get feature layer.
	layer = sf.GetLayer(0)

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

		if (counter % 1000) == 0: print "%s" % (counter),
		counter += 1

		# Get feature attributes.
		f_attributes = {}
		for i in range(field_count): 
			f_attributes[fields[i]] = f.GetField(i)

		# Skip blank rows.
		if (not f_attributes['SOURCE']): continue

		# Get feature geometry. We convert each feature into a multipolygon, since
		# we may have a mix of normal polygons and multipolygons.
		geom = wkb.loads(f.GetGeometryRef().ExportToWkb())
		if geom.geom_type =='Polygon':
			geom = MultiPolygon([(geom.exterior.coords, geom.interiors )])

		# Get habitat's energy code.
		energy = energy_mappings.shp_to_va[f_attributes['Energy']] 
		
		# Create habitat's substrate object.
		substrate_id = substrate_mappings.shp_to_va[f_attributes['TYPE_SUB'].strip()]
		substrate = session.query(Substrate).filter(Substrate.id == substrate_id).one()

		# Get habitat's feature assignments, based on substrate and energy.
		assignments = feature_assignments.assignments[(substrate_id, energy)]

		# Create features from assignments
		features = session.query(Feature).filter(Feature.id.in_(assignments)).all()

		# Make habitat object from feature data.
		h = Habitat(
				id_km100 = f_attributes['100km_Id'],
				id_km1000 = f_attributes['1000Km_Id'],
				id_vor = f_attributes['Vor_id'],
				z = f_attributes['z'],
				energy = f_attributes['Energy'],
				substrate = substrate,
				features = features,
				area = f_attributes['Area_Km'],	
				geom = geom.wkt
				)

		habitats.append(h)	

	
	print "Writing habitats to db"
	# Write habitats to db
	session.add_all(habitats)
	session.commit()

	print "Calculating areas for habitats."
	habitat_area = geo_func.area(Habitat.geom).label('habitat_area')
	habitat_infos = session.query(Habitat, habitat_area).all()
	for (habitat, habitat_area) in habitat_infos:
		habitat.area = habitat_area
	session.commit()

	print "done"

if __name__ == '__main__':
	main()
