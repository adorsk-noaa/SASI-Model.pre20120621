import shapely.wkb
import json
import tempfile
import zipfile
import os

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
		if field == 'features': return self.format_features(habitat.habitat_type.features)

	def format_features(self, features):
		return json.dumps([{
			'id': feature.id,
			'name': feature.name,
			'category': feature.category,
			} for feature in features])

	def mkdtemp(self, *args, **kwargs):
		return tempfile.mkdtemp(*args, **kwargs)
	

	def make_package(self, export_dir=None, package_name="habitats"):
		# create zip file from export files.
		zfile_path = tempfile.mktemp(suffix=".zip")
		zfile_h = zipfile.ZipFile(zfile_path, "w")
		for f in os.listdir(export_dir):
			zfile_h.write("{}/{}".format(export_dir, f), "{}/{}".format(package_name, os.path.basename(f)))
		zfile_h.close()
		return zfile_path

