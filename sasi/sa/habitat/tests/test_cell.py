import unittest
from sasi.sa.tests.basetest import BaseTest
import sasi.sa.habitat.cell as sa_cell
import sasi.sa.habitat.habitat as sa_habitat
import sasi.sa.habitat.feature as sa_feature
import sasi.sa.habitat.substrate as sa_substrate
import sasi.util.habitat.habitat as habitat_util
from sasi.habitat.cell import Cell

from sqlalchemy import MetaData
from geoalchemy import *
from geoalchemy.geometry import Geometry

class CellTest(BaseTest):

	def test(self):
		s = self.session

		# Combine tables into one metadata
		# in order to resolve dependencies.
		combined_metadata = MetaData()
		for m in [sa_cell, sa_habitat, sa_feature, sa_substrate]:
			for t in m.metadata.tables.values():
				new_t = t.tometadata(combined_metadata)

				# Run DDL if table has geometry columns.
				has_geom = False
				for c in new_t.columns:
					if isinstance(c.type, Geometry): has_geom = True
				if has_geom: GeometryDDL(new_t)

		# Drop/Create tables.
		combined_metadata.drop_all(s.bind)
		combined_metadata.create_all(s.bind)
		# Generate test cell
		cell = habitat_util.generate_cells(1).pop()

		# Add cell's habitats to the session.
		for h in cell.habitats:
			s.merge(h)

		# Add to the session and commit.
		s.merge(cell)
		s.commit()

		cells = s.query(Cell).all()

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()
	
