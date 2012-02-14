import unittest
import sasi.util.habitat.habitat  as habitat_util

class HabitatUtilTest(unittest.TestCase):

	def test(self):

		habitats = habitat_util.generate_habitats()
		regions = habitat_util.generate_regions(10)
		cells = habitat_util.generate_cells(10)

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()




