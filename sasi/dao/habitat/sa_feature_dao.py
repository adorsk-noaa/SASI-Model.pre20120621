import sasi.sa.habitat.feature as sa_feature
from sasi.dao.habitat.feature_dao import Feature_DAO
from sasi.habitat.feature import Feature


class SA_Feature_DAO(Feature_DAO):

	def __init__(self, session=None):
		self.session = session

	def get_features(self, filters=None):
		q = self.session.query(Feature)
		if filters:
			for filter_name, filter_values in filters.items():
				q = q.filter(getattr(Feature, filter_name).in_(filter_values))

		return q.all()
