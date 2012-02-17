import unittest
from sasi.sa.tests.basetest import BaseTest
from sasi.results.persistent_sasi_result_collection import Persistent_SASI_Result_Collection
from sasi.dao.results.sa_sasi_result_collection_dao import SA_SASI_Result_Collection_DAO
import sasi.sa.metadata as sa_metadata
import sasi.util.results.results as results_util

class Persistent_SASI_Result_Collection_Test(BaseTest):

	def test(self):

		# Clean tables.
		sa_metadata.metadata.drop_all(self.session.bind)
		sa_metadata.metadata.create_all(self.session.bind)

		results = results_util.generate_sasi_results(10)

		dao = SA_SASI_Result_Collection_DAO(session = self.session)

		collection = Persistent_SASI_Result_Collection(id = 'test', dao = dao)
		collection.add_results(results)
		filtered_results = collection.get_results(filters = {'time': ['0']})
		collection.delete_results(results=filtered_results)
		collection.delete()

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()




