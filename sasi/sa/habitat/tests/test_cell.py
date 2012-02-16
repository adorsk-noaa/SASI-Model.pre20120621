import unittest
from sasi.sa.tests.basetest import BaseTest
import sasi.sa.metadata as sa_metadata
import sasi.sa.habitat.cell as sa_cell
import sasi.util.habitat.habitat as habitat_util

from sasi.habitat.cell import Cell

from sqlalchemy import MetaData
from geoalchemy import *
from geoalchemy.geometry import Geometry

class CellTest(BaseTest):

	def test(self):
		s = self.session

		# Drop/Create tables.
		sa_metadata.metadata.drop_all(s.bind)
		sa_metadata.metadata.create_all(s.bind)
		
		# Generate test cell
		cell = habitat_util.generate_cells(1).pop()

		# Add to the session and commit.
		s.merge(cell)
		s.commit()

		cells = s.query(Cell).all()

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()
	
