import unittest
from sasi.sa.tests.basetest import BaseTest
import sasi.sa.metadata as sa_metadata
import sasi.sa.all_metadata
import sasi.util.fishing.fishing as fishing_util

from sasi.fishing.effort import Effort
from sasi.fishing.effort_set import Effort_Set

class SA_Effort_Set_Test(BaseTest):

	def test(self):
		s = self.session

		# Drop/Create tables.
		sa_metadata.metadata.drop_all(s.bind)
		sa_metadata.metadata.create_all(s.bind)
		s.commit()
		
		# Generate test effort set.
		effort_sets = fishing_util.generate_effort_sets(2)

		# Add to the session and commit.
		for es in effort_sets:
			s.add(es)
			s.commit()

		fetched_es = s.query(Effort_Set).all()

		efforts_for_es0 = s.query(Effort).join(Effort_Set.efforts).filter(Effort_Set.id == fetched_es[0].id).all()

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()
	
