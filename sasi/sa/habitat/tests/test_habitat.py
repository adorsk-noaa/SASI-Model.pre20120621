import unittest
from sasi.sa.tests.basetest import BaseTest
import sasi.sa.metadata as sa_metadata
import sasi.sa.all_metadata
import sasi.sa.habitat.habitat as sa_habitat
from sasi.habitat.habitat import Habitat
import sasi.util.habitat.habitat as habitat_util

from sqlalchemy import MetaData
from geoalchemy import *
from geoalchemy.geometry import Geometry

class HabitatTest(BaseTest):

	def test(self):
		s = self.session

		# Drop/Create tables.
		sa_metadata.metadata.drop_all(s.bind)
		sa_metadata.metadata.create_all(s.bind)

		# Generate test habitat
		h = habitat_util.generate_habitats(1).pop()

		# Add to the session and commit.
		s.add(h)
		s.commit()

		h2 = s.query(Habitat).filter(Habitat.id == h.id).one()

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()
	
