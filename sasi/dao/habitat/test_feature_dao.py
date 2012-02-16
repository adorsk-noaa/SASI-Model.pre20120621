from sasi.dao.habitat.feature_dao import Feature_DAO
import sasi.util.habitat.habitat as habitat_util


class Test_Feature_DAO(Feature_DAO):

	def __init__(self, num_features=10):
		self.features = {}

		n = 0
		for f in habitat_util.generate_features(num_features):
			self.features[n] = f
			n += 1		

	def get_features(self, filters=None):

		# By default, get all habitats.
		features = self.features.values()

		# Apply filters.
		if filters:
			for filter_name, filter_values in filters.items():
				features = [f for f in self.features if getattr(f, filter_name) in filter_values]

		return features
