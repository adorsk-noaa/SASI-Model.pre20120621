import shapely.wkb
import json

class Exporter(object):

	def __init__(self):
		self.generic_fields = [
				'id',
				'geom',
				]

	def get_field(self, habitat, field):
		if field in self.generic_fields: return getattr(habitat, field)
		if field == 'substrate_name': return habitat.habitat_type.substrate.name
		if field == 'substrate_id': return habitat.habitat_type.substrate.id
		if field == 'energy': return habitat.habitat_type.energy
		if field == 'depth_meters': return -1.0 * habitat.z
		if field == 'area_meters2': return habitat.area
		if field == 'geom_wkt': return shapely.wkb.loads(str(habitat.geom.geom_wkb)).wkt
		if field == 'features': return [self.format_feature(feature) for feature in habitat.habitat_type.features]

	def format_feature(self, feature):
		return json.dumps({
			'id': feature.id,
			'name': feature.name,
			'category': feature.category,
			})


