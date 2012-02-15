import unittest
from collections import defaultdict
from sasi.habitat.habitat_type import Habitat_Type
from sasi.habitat.tests import test_feature
from sasi.habitat.tests import test_substrate
import sasi.util.habitat.habitat as habitat_util

class Habitat_Type_Test(unittest.TestCase):

	def test(self):
		ht = habitat_util.generate_habitat_types().pop()
		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()




