import sasi.sa.results.sasi_resultas sa_sasi_result
import sasi.sa.results.sasi_result_collection as sa_sasi_result_collection
from sasi.results.sasi_result import SASI_Result
from sasi.results.sasi_result_collection import SASI_Result_Collection

class SA_SASI_Result_DAO(object):

	def __init__(self, session=None):
		self.session = session

	def get_results(self, filters=None):
		q = self.session.query(SASI_Result)
		if filters:
			for filter_name, filter_values in filters.items():
				if filter_name == 'sasi_result_collection':
					q = q.join(SASI_Result_Collection).filter(SASI_Result_Collection.id.in_(filter_values))
				else:
					q = q.filter(getattr(SASI_Result, filter_name).in_(filter_values))

		return q.all()

	def save_results(self): pass

	def update_results(self): pass

	def delete_results(self): pass
