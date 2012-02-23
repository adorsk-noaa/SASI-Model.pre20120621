import unittest
from sasi.sa.tests.basetest import BaseTest
import sasi.sa.metadata as sa_metadata
import sasi.sa.all_metadata
import sasi.util.results.results as results_util
import sasi.util.registry as util_registry

from sasi.dao.results.sa_result_dao import SA_Result_DAO

from sasi.results.result import Result
from sasi.results.result_set import Result_Set

class SA_Result_Set_Test(BaseTest):

	def test(self):
		s = self.session
		dao = SA_Result_DAO(session = s)

		# Drop/Create tables.
		sa_metadata.metadata.drop_all(s.bind)
		sa_metadata.metadata.create_all(s.bind)
		s.commit()
		
		# Generate test result set.
		result_sets = results_util.generate_result_sets(2)

		## Merge generated objects for testing.
		for o_key, o in util_registry.object_registry.items():
			try:
				if not o_key[0] in ['Result', 'Result_Set']:
					s.add(o)
			except: pass
		s.commit()

		# Test DAO operations.
		dao.save_result_sets(result_sets)
		fetched_result_sets = dao.get_result_sets(filters=[{'attr':'id', 'op': 'in', 'value': [result_sets[0].id]}])
		fetched_results = dao.get_results(filters=[{'attr':'result_sets', 'value': [result_sets[1]]}])
		new_rs = dao.get_results_as_result_set(result_set_id='morfog', filters=[{'attr': 'result_sets', 'value': [result_sets[1]]}])
		dao.save_result_sets([new_rs])
		fetched_results_new_rs = dao.get_results(filters=[{'attr': 'result_sets', 'value': [new_rs]}])
		field_density_by_t_c = dao.get_field_density_by_t_c(filters=[{'attr': 'result_sets', 'value': [new_rs]}])
		values_by_t_c_f = dao.get_values_by_t_c_f(filters=[{'attr': 'result_sets', 'value': [new_rs]}])

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()
	
