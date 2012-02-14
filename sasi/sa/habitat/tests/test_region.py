import unittest
from sasi.sa.tests.basetest import BaseTest
import sasi.sa.metadata as sa_metadata
import sasi.sa.habitat.region as sa_region
import sasi.util.habitat.habitat as habitat_util

from sqlalchemy import MetaData
from geoalchemy import *
from geoalchemy.geometry import Geometry

class RegionTest(BaseTest):

	def test(self):
		s = self.session

		# Drop/Create tables.
		sa_metadata.metadata.drop_all(s.bind)
		sa_metadata.metadata.create_all(s.bind)

		# Generate test region
		r = habitat_util.generate_regions(1).pop()

		# Add to the session and commit.
		s.add(r)
		s.commit()

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()
	
