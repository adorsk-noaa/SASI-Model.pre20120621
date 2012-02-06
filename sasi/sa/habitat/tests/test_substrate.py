import unittest
from sasi.sa.tests.basetest import BaseTest
import sasi.sa.habitat.substrate as sa_substrate
from sasi.habitat.substrate import Substrate
import sasi.habitat.tests.test_substrate as test_substrate

class SubstrateTest(BaseTest):

	def test(self):
		substrates = test_substrate.generate_substrates(1)
		s = self.session
		sa_substrate.metadata.create_all(s.bind)
		s.add_all(substrates)
		s.commit()
		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()
	
