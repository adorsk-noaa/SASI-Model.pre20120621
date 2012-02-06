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

import ogr
from shapely import wkb
from shapely.geometry import Polygon, MultiPolygon

def main():


	# Get db session.
	session = sa_session.get_session()

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
	i = 0
	for f in layer:

		#if i > 1: break
		print "Assembling %d" % i
		i += 1
		
		
		# Get feature geometry. We convert each feature into a multipolygon, since
		# we may have a mix of normal polygons and multipolygons.
		geom = wkb.loads(f.GetGeometryRef().ExportToWkb())
		if geom.geom_type =='Polygon':
			geom = MultiPolygon([(geom.exterior.coords, geom.interiors )])

		# Get feature attributes.
		f_attributes = {}
		for i in range(field_count): 
			f_attributes[fields[i]] = f.GetField(i)

		# Skip blank rows.
		if (not f_attributes['SOURCE']): continue

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

	print "Clearing db"
	# Clear db of cells.
	sa_habitat.metadata.drop_all(bind = session.connection())
	sa_habitat.metadata.create_all(bind = session.connection())
	session.commit()
	
	print "Saving to db"
	# Write habitats to db
	session.add_all(habitats)
	session.commit()


	print "done"

if __name__ == '__main__':
	main()
