import unittest
import sasi.util.fishing.fishing as fishing_util

class Fishing_Util_Test(unittest.TestCase):

	def test(self):

		gears = fishing_util.generate_gears()

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()




