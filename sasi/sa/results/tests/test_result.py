import unittest
from sasi.sa.tests.basetest import BaseTest
import sasi.sa.metadata as sa_metadata
import sasi.sa.all_metadata
import sasi.util.results.results as results_util

from sasi.results.result import Result
from sasi.results.result_set import Result_Set

class SA_Result_Test(BaseTest):

	def test(self):
		s = self.session

		# Drop/Create tables.
		sa_metadata.metadata.drop_all(s.bind)
		sa_metadata.metadata.create_all(s.bind)
		s.commit()
		
		# Generate test result
		result = results_util.generate_results(1).pop()

		# Add to the session and commit.
		s.add(result)
		s.commit()

		# Get results.
		fetched_results = s.query(Result).all()

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()
	
