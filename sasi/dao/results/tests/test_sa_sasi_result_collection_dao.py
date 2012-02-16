import unittest
from sasi.sa.tests.basetest import BaseTest
import sasi.sa.metadata as sa_metadata
import sasi.sa.habitat.habitat_metadata
import sasi.util.results.results as results_util

from sasi.dao.results.sa_sasi_result_collection_dao import SA_SASI_Result_Collection_DAO

class SA_SASI_Result_Collection_DAO_Test(BaseTest):

	def test(self):
		s = self.session

		sa_metadata.metadata.drop_all(s.bind)
		sa_metadata.metadata.create_all(s.bind)
		s.commit()

		sasi_result_collection_dao = SA_SASI_Result_Collection_DAO(session = s)
		
		collections = results_util.generate_sasi_result_collections(2)

		# Merge cells for testing.
		for c in collections:
			for r in c.results:
				s.merge(r.cell)
		s.commit()
			

		sasi_result_collection_dao.save_collection(collections[0])
		sasi_result_collection_dao.save_collection(collections[1])
		results = sasi_result_collection_dao.get_collection_results(collections[1], filters={'time': ['0']})
		sasi_result_collection_dao.delete_collection_results(collections[1], results)
		collections[1] = sasi_result_collection_dao.get_collections(filters={'id': [collections[1].id]}).pop()

if __name__ == '__main__':
	unittest.main()
