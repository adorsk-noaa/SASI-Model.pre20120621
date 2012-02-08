import unittest

from sasi.dao.habitat.test_cell_dao import Test_Cell_DAO
from sasi.habitat.static_grid_model import StaticGridModel

class StaticGridModelTest(unittest.TestCase):

	def test(self):
		grid_model = StaticGridModel(cell_dao=Test_Cell_DAO()) 

		cells = grid_model.get_cells()

if __name__ == '__main__':
	unittest.main()
