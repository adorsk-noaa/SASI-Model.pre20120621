import unittest
from collections import defaultdict
from sasi.habitat.cell import Cell

class CellTest(unittest.TestCase):

	def test(self):
		c = self.generateCells(1).pop()
		print c

		self.failUnless(True)

	def generateCells(self,n):
		cells = []
		for i in range(0,n):
			c = Cell()
			cells.append(c)
		return cells
			

if __name__ == '__main__':
	unittest.main()




