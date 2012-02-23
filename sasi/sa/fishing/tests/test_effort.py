import unittest
from sasi.sa.tests.basetest import BaseTest
import sasi.sa.metadata as sa_metadata
import sasi.sa.all_metadata
import sasi.util.fishing.fishing as fishing_util

from sasi.fishing.effort import Effort

class SA_Effort_Test(BaseTest):

	def test(self):
		s = self.session

		# Drop/Create tables.
		sa_metadata.metadata.drop_all(s.bind)
		sa_metadata.metadata.create_all(s.bind)
		s.commit()
		
		# Generate test result
		effort = fishing_util.generate_efforts(1).pop()

		# Add to the session and commit.
		s.add(effort)
		s.commit()

		# Get efforts.
		fetched_efforts = s.query(Effort).all()

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()
	
