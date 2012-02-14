import unittest

from sasi.habitat.static_grid_model import StaticGridModel
from sasi.dao.habitat.test_cell_dao import Test_Cell_DAO

class StaticGridModelTest(unittest.TestCase):

	def test(self):
		grid_model = StaticGridModel(cell_dao=Test_Cell_DAO(), default_filters={'type': ['km100']}) 

		cells = grid_model.get_cells()

if __name__ == '__main__':
	unittest.main()
