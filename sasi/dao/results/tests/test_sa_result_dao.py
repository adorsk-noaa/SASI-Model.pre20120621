import unittest
from sasi.sa.tests.basetest import BaseTest
import sasi.sa.metadata as sa_metadata
import sasi.sa.all_metadata
import sasi.util.results.results as results_util
import sasi.util.registry as util_registry

from sasi.dao.results.sa_result_dao import SA_Result_DAO

from sasi.results.result import Result

class SA_Result_Set_Test(BaseTest):

	def test(self):
		s = self.session
		dao = SA_Result_DAO(session = s)

		# Drop/Create tables.
		sa_metadata.metadata.drop_all(s.bind)
		sa_metadata.metadata.create_all(s.bind)
		s.commit()
		
		# Generate test result set.
		results = results_util.generate_results()

		## Merge generated objects for testing.
		for o_key, o in util_registry.object_registry.items():
			try:
				if not o_key[0] in ['Result']:
					s.add(o)
			except: pass
		s.commit()

		# Test DAO operations.
		dao.save_results(results)
		fetched_results = dao.get_results(filters=[
			{
				'field': 'tag',
				'op': '==',
				'value': 'a'
				}
			])

		result_field = {
				'field': 'a',
				'aggregate_funcs': ['sum']
				}

		mapserver_data_string = dao.get_mapserver_data_string(result_field=result_field)
		print mapserver_data_string

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()
	
