import unittest
from sasi.sa.tests.basetest import BaseTest
import sasi.sa.metadata as sa_metadata
import sasi.sa.habitat.habitat_metadata
import sasi.sa.habitat.substrate as sa_substrate
import sasi.util.habitat.habitat as habitat_util

class Substrate_Test(BaseTest):

	def test(self):
		s = self.session
		sa_metadata.metadata.drop_all(s.bind)
		sa_metadata.metadata.create_all(s.bind)

		substrate = habitat_util.generate_substrates(1).pop()

		s.merge(substrate)
		s.commit()
		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()
	
