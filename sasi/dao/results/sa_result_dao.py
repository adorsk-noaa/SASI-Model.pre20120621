import sasi.sa.results.result
import sasi.sa.results.result_set
from sasi.results.result import Result
from sasi.results.result_set import Result_Set

class SA_Result_DAO(object):

	def __init__(self, session=None):
		self.session = session

	def get_results(self, filters=None):
		q = self.get_filtered_results_query(filters=filters)
		return q.all()

	def get_results_as_result_set(self, result_set_id=None, filters=None):
		q = self.get_filtered_results_query(filters=filters)
		return Result_Set(
				id = result_set_id,
				results = q.all()
				)

	def save_results(self, results, commit=True):
		self.session.add_all(results)
		if commit: self.session.commit()

	def delete_results(self, filters=None, commit=True):
		q = self.get_filtered_results_query(filters=filters)
		q.delete()
		if commit: self.session.commit()
	
	def get_result_sets(self, filters=None):
		q = self.get_filtered_result_sets_query(filters)
		return q.all()

	def delete_result_sets(self, filters=None, commit=True):
		q = self.get_filtered_result_sets_query(filters)
		q.delete()
		if commit: self.session.commit()

	def save_result_sets(self, result_sets, commit=True):
		for result_set in result_sets:
			self.session.add(result_set)
		if commit: self.session.commit()
	
	def get_filtered_results_query(self, filters=None):
		q = self.session.query(Result)
		if filters:
			for filter_name, filter_values in filters.items():

				if filter_name == 'result_set_id':
					q = q.join(Result_Set.results).filter(Result_Set.id.in_(filter_values))
				elif filter_name == 'result_set':
					q = q.join(Result_Set.results).filter(Result_Set.id.in_([rs.id for rs in filter_values]))
				elif filter_name == 'results':
					q = q.filter(Result.id.in_([result.id for result in filter_values]))
				else:
					q = q.filter(getattr(Result, filter_name).in_(filter_values))
		return q

	def get_filtered_result_sets_query(self, filters=None):
		q = self.session.query(Result_Set)
		if filters:
			for filter_name, filter_values in filters.items():
				q = q.filter(getattr(Result_Set, filter_name).in_(filter_values))
		return q
