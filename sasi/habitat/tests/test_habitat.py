import unittest
from collections import defaultdict
from sasi.habitat.habitat import Habitat
from sasi.habitat.tests import test_feature
from sasi.habitat.tests import test_substrate
import sasi.util.habitat.habitat as habitat_util

class HabitatTest(unittest.TestCase):

	def test(self):
		h = habitat_util.generate_habitats().pop()
		print h
		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()




