import unittest
from sasi.sa.tests.basetest import BaseTest
import sasi.sa.metadata as sa_metadata
import sasi.sa.fishing.gear as sa_gear
import sasi.util.fishing.fishing as fishing_util
from sasi.fishing.gear import Gear

class Gear_Test(BaseTest):

	def test(self):
		s = self.session
		sa_metadata.metadata.drop_all(s.bind)
		sa_metadata.metadata.create_all(s.bind)

		gear = fishing_util.generate_gears().pop()
		s.add(gear)
		s.commit()
		s.query(Gear)

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()
	
