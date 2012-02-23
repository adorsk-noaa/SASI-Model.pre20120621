import unittest
from sasi.sa.tests.basetest import BaseTest
import sasi.sa.metadata as sa_metadata
import sasi.sa.all_metadata
import sasi.util.fishing.fishing as fishing_util
import sasi.util.registry as util_registry

from sasi.dao.fishing.sa_effort_dao import SA_Effort_DAO

from sasi.fishing.effort import Effort
from sasi.fishing.effort_set import Effort_Set

class SA_Effort_Set_Test(BaseTest):

	def test(self):
		s = self.session
		dao = SA_Effort_DAO(session = s)

		# Drop/Create tables.
		sa_metadata.metadata.drop_all(s.bind)
		sa_metadata.metadata.create_all(s.bind)
		s.commit()
		
		# Generate test effort set.
		effort_sets = fishing_util.generate_effort_sets(2)

		## Merge generated objects for testing.
		for o_key, o in util_registry.object_registry.items():
			try:
				if not o_key[0] in ['Effort', 'Effort_Set']:
					s.add(o)
			except: pass
		s.commit()

		# Test DAO operations.
		dao.save_effort_sets(effort_sets)
		fetched_effort_sets = dao.get_effort_sets(filters=[{'attr':'id', 'value': [effort_sets[0].id]}])
		fetched_efforts = dao.get_efforts(filters=[{'attr':'effort_sets', 'value': [effort_sets[1]]}])
		new_es = dao.get_efforts_as_effort_set(effort_set_id='morfog', filters=[{'attr': 'effort_sets', 'value': [effort_sets[1]]}])
		dao.save_effort_sets([new_es])
		fetched_efforts_new_es = dao.get_efforts(filters=[{'attr': 'effort_sets', 'value': [new_es]}])
		fetched_effort = dao.get_efforts(filters=[{'attr': 'id', 'op': '==', 'value': fetched_efforts[0].id}])


		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()
	
