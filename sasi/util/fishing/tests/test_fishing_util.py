import unittest
import sasi.util.fishing.fishing as fishing_util

class Fishing_Util_Test(unittest.TestCase):

	def test(self):

		gears = fishing_util.generate_gears()
		efforts = fishing_util.generate_efforts(n=10)
		effort_sets = fishing_util.generate_effort_sets(n=1)

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()




