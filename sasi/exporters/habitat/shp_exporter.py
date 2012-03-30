import exporter as habitat_exporter
from fiona import collection
from fiona.ogrext import GeomBuilder

class ShpExporter(habitat_exporter.Exporter):

	def __init__(self):
		habitat_exporter.Exporter.__init__(self)
	
	def export(self, habitats=[]):

		# Make tmpdir to hold export.
		tmp_dir = self.mkdtemp()

		shapefile = "{}/{}".format(tmp_dir, "habitats.shp")

		# Mapping from truncated names to full field names.
		# Shapefile column names can only be 10 chars. >:(
		truncated_names = {
				'id': 'id',
				'sstrt_nm': 'substrate_name',
				'sstrt_id': 'substrate_id',
				'energy': 'energy',
				'features': 'features',
				'depth_m': 'depth_meters',
				'area_m2': 'area_meters2',
				}

		# Define shapefile schema.
		schema = {
				'geometry': 'MultiPolygon',
				'properties': {
					'id': 'int',
					'sstrt_nm': 'str',
					'sstrt_id': 'str',
					'energy': 'str',
					'features': 'str',
					'depth': 'float',
					'area': 'float',
					}
				}

		# Write shpfile.
		driver = 'ESRI Shapefile'
		crs = {'init': "epsg:4326"}

		with collection(shapefile, "w", driver=driver, schema=schema, crs=crs) as c:
			for habitat in habitats:

				# Populate record properties.
				properties = {}
				for p, p_type in schema['properties'].items():
					full_field_name = truncated_names[p]
					properties[p] = __builtins__.get(p_type)(self.get_field(habitat, full_field_name))

				# Populate record geometry.
				geometry = GeomBuilder().build_wkb("{!s}".format(habitat.geom.geom_wkb))

				# Assemble the record.
				record = {
						'id': properties['id'],
						'geometry': geometry,
						'properties': properties
						}

				# Write the record.
				c.write(record)

		# Package the export.
		package_file = self.make_package(export_dir=tmp_dir)

		return package_file

	# Custom feature formatting, for just feature ids.
	def format_features(self, features):
		return ','.join([feature.id for feature in features])
