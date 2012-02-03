import unittest
import sasi.sqlalchemy.session as sa_session
import sasi.sqlalchemy.engine as sa_engine
import sasi.sqlalchemy.habitat.cell as sa_cell
from sasi.habitat.cell import Cell

class CellTest(unittest.TestCase):

	def test(self):
		s = sa_session.get_session()
		sa_cell.metadata.create_all(s.bind)
		c = Cell(geom='MULTIPOLYGON(((0 0, 1 0, 1 1, 0 1, 0 0)))')
		s.add(c)
		s.commit()
		print "c is: %s" % c.id_100km
		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()
	
