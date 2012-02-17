import unittest
from sasi.sa.tests.basetest import BaseTest
import sasi.sa.metadata as sa_metadata
import sasi.sa.all_metadata
import sasi.util.results.results as results_util

from sasi.results.result import Result
from sasi.results.result_set import Result_Set

class SA_Result_Set_Test(BaseTest):

	def test(self):
		s = self.session

		# Drop/Create tables.
		sa_metadata.metadata.drop_all(s.bind)
		sa_metadata.metadata.create_all(s.bind)
		s.commit()
		
		# Generate test result collection.
		result_sets = results_util.generate_result_sets(2)

		# Add to the session and commit.
		for rs in result_sets:
			s.add(rs)
			s.commit()

		fetched_rs = s.query(Result_Set).all()

		results_for_rs0 = s.query(Result).join(Result_Set.results).filter(Result_Set.id == fetched_rs[0].id).all()

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()
	
