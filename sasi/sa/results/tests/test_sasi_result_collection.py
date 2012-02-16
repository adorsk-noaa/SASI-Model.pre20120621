import unittest
from sasi.sa.tests.basetest import BaseTest
import sasi.sa.metadata as sa_metadata
import sasi.sa.habitat.cell as sa_cell
import sasi.sa.results.sasi_result_collection as sa_sasi_result_collection
import sasi.util.results.results as results_util

from sasi.results.sasi_result_collection import SASI_Result_Collection

class SASI_Result_Collection_Test(BaseTest):

	def test(self):
		s = self.session

		# Drop/Create tables.
		sa_metadata.metadata.drop_all(s.bind)
		sa_metadata.metadata.create_all(s.bind)
		
		# Generate test result collection.
		sasi_result_collection = results_util.generate_sasi_result_collections(1).pop()

		# Merge cells to avoid primary key conflicts.
		for r in sasi_result_collection.results:
			s.merge(r.cell)

		# Add to the session and commit.
		s.merge(sasi_result_collection)
		s.commit()

		rc = s.query(SASI_Result_Collection).all()

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()
	
