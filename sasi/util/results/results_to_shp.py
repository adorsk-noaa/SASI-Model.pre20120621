import sasi.conf.conf as conf

import sasi.sa.session as sa_session

from sasi.dao.results.sa_result_dao import SA_Result_DAO

from sasi.results.result_set import Result_Set

from fiona import collection
from fiona.ogrext import GeomBuilder

def main():

	output_dir = '/home/adorsk/projects/sasi/sasi_model/outputs/shapefiles'

	result_set_id = 'g3_c0-5'

	times = ['5']

	# Get result dao.
	db_session = sa_session.get_session()
	result_dao = SA_Result_DAO(session=db_session)

	# Load result set via DAO.
	result_set = result_dao.get_result_sets(filters={'id': [result_set_id]}).pop()
	
	# Get field densities by time, cell, and field for result set.
	fd_by_t_c_f = result_dao.get_field_density_by_t_c(filters={'result_set': [result_set]})

	#
	# Make fiona collection from result set.
	#

	# Define schema.
	geometry_type = 'MultiPolygon'
	schema = {
			'geometry': geometry_type,
			'properties': {
				'type_id': 'str',
				'ht': 'str'
				}
			}
	generic_attrs = ['A', 'Y', 'X', 'Z', 'ZZ']
	for generic_attr in generic_attrs: schema['properties'][generic_attr] = 'float'

	# For each time...
	for t in times:

		# Write shpfile.
		filename = "%s/%s.%s.shp" % (output_dir, result_set_id, t) 
		driver = 'ESRI Shapefile'
		crs = {'no_defs': True, 'ellps': 'GRS80', 'datum': 'NAD83', 'proj': 'utm', 'zone': 19, 'units': 'm'}

		with collection(
				filename, "w",
				driver=driver,
				schema=schema,
				crs=crs
				) as c:
			record_counter = 1
			for cell, cell_fields in fd_by_t_c_f[t].items():

				# Populate record properties.
				habitat_types = set(["(%s)" % h.habitat_type.id for h in cell.habitats])
				properties = {
						'type_id': cell.type_id,
						'ht': ' & '.join(habitat_types)
						}
				for generic_attr in generic_attrs:
					properties[generic_attr] = cell_fields.get(generic_attr,0.0)

				# Populate record geometry.
				wkb_geom = "%s" % cell.geom.geom_wkb
				geometry = GeomBuilder().build_wkb(wkb_geom)

				# Assemble the record.
				record = {
						'id': record_counter,
						'geometry': geometry,
						'properties': properties
						}

				# Write the record.
				c.write(record)
				record_counter += 1

if __name__ == '__main__': main()
