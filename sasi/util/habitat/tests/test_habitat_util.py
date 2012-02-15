import unittest
import sasi.util.habitat.habitat  as habitat_util

class HabitatUtilTest(unittest.TestCase):

	def test(self):

		habitat_types = habitat_util.generate_habitat_types()
		habitats = habitat_util.generate_habitats(10)
		cells = habitat_util.generate_cells(10)

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()




