import sasi.conf.conf as conf

import sasi.sa.session as sa_session

from sasi.dao.results.sa_result_dao import SA_Result_DAO

from sasi.results.result import Result

from fiona import collection
from fiona.ogrext import GeomBuilder

import sys

def main():

	output_dir = '/home/adorsk/projects/sasi/sasi_model/outputs/shapefiles'

	result_tag = 'gc30_all'

	t = 1999

	# Get result dao.
	db_session = sa_session.get_session()
	result_dao = SA_Result_DAO(session=db_session)

	# Get values by time, cell, and field for results.
	values_by_t_c_f = result_dao.get_values_by_t_c_f(filters=[
		{'attr': 'tag', 'op': '==', 'value': result_tag}, 
		{'attr': 'time', 'op': '==', 'value': t}
		])

	#
	# Make fiona collection from result set.
	#

	# Define schema.
	geometry_type = 'MultiPolygon'
	schema = {
			'geometry': geometry_type,
			'properties': {
				'type_id': 'str',
				'hab_type': 'str'
				}
			}
	generic_attrs = ['A', 'Y', 'X', 'Z', 'ZZ']
	for generic_attr in generic_attrs: schema['properties'][generic_attr] = 'float'

	# Write shpfile.
	filename = "%s/%s.%s.shp" % (output_dir, result_tag, t) 
	driver = 'ESRI Shapefile'
	crs = {'init': "epsg:4326"}

	with collection(
			filename, "w",
			driver=driver,
			schema=schema,
			crs=crs
			) as c:
		record_counter = 1
		for cell, cell_fields in values_by_t_c_f[t].items():

			if (record_counter % 1000) == 0:
				print >> sys.stderr, "%s" % record_counter

			# Populate record properties.
			habitat_types = set(["(%s)" % h.habitat_type.id for h in cell.habitats])
			properties = {
					'type_id': cell.type_id,
					'hab_type': ' & '.join(habitat_types)
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
