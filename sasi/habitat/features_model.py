class Features_Model(object):

	def __init__(self, feature_dao=None, default_filters=None):
		self.feature_dao = feature_dao
		self.default_filters = default_filters

	def get_features(self, filters=None, override_default_filters=False):

		if self.default_filters and not filters:
			return self.feature_dao.get_cells(filters=self.default_filters)

		elif self.default_filters and filters and not override_default_filters:
			combined_filters = self.default_filters.copy()
			combined_filters.update(filters)
			return self.feature_dao.get_features(filters=combined_filters)

		else:
			return self.feature_dao.get_features(filters=filters)

