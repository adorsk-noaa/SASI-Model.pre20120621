import unittest
from sasi.sqlalchemy.tests.basetest import BaseTest
import sasi.sqlalchemy.habitat.cell as sa_cell
from sasi.habitat.cell import Cell

class CellTest(BaseTest):

	def test(self):
		s = self.session
		sa_cell.metadata.create_all(s.bind)
		c = Cell(geom='MULTIPOLYGON(((0 0, 1 0, 1 1, 0 1, 0 0)))')
		s.add(c)
		s.commit()
		print "c is: %s" % c.id_100km
		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()
	
