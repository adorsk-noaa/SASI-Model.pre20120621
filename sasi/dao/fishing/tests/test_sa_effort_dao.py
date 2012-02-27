import unittest
from sasi.sa.tests.basetest import BaseTest
import sasi.sa.metadata as sa_metadata
import sasi.sa.all_metadata
import sasi.util.fishing.fishing as fishing_util
import sasi.util.registry as util_registry

from sasi.dao.fishing.sa_effort_dao import SA_Effort_DAO

from sasi.fishing.effort import Effort

class SA_Effort_Set_Test(BaseTest):

	def test(self):
		s = self.session
		dao = SA_Effort_DAO(session = s)

		# Drop/Create tables.
		sa_metadata.metadata.drop_all(s.bind)
		sa_metadata.metadata.create_all(s.bind)
		s.commit()
		
		# Generate test effort set.
		efforts = fishing_util.generate_efforts()

		## Merge generated objects for testing.
		for o_key, o in util_registry.object_registry.items():
			try:
				if not o_key[0] in ['Effort']:
					s.add(o)
			except: pass

		# Test DAO operations.
		dao.save_efforts(efforts)
		fetched_efforts = dao.get_efforts()

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()
	
