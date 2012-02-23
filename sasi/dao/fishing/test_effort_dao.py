from sasi.dao.fishing.effort_dao import Effort_DAO
import sasi.util.fishing.fishing as fishing_util


class Test_Effort_DAO(Effort_DAO):

	def __init__(self, num_effort_sets=2, efforts_per_set=10):
		self.effort_sets = fishing_util.generate_effort_sets(num_effort_sets, efforts_per_set)

	def get_efforts(self, filters=None):
		efforts = []
		for es in self.effort_sets: efforts.extend(es.efforts)

		# Only handle certain filters.
		if filters:
			for f in filters:

				if f['attr'] == 'effort_sets':
					for es in f['value']:
						efforts = filter(lambda e: e in es, efforts)
					
		return efforts

	def get_efforts_as_effort_set(self, effort_set_id=None, filters=None):
		return Effort_Set(
				id = effort_set_id,
				efforts = self.get_efforts(get_efforts)
				)

	def save_efforts(self, efforts, commit=True): pass

	def delete_efforts(self, filters=None, commit=True): pass
	
	def get_effort_sets(self, filters=None):
		return self.effort_sets

	def delete_effort_sets(self, filters=None, commit=True): pass

	def save_effort_sets(self, effort_sets=None, commit=True): pass
	
