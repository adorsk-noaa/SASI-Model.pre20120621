import unittest

from sasi.dao.habitat.test_cell_dao import Test_Cell_DAO
from sasi.dao.va.csv_va_dao import CSV_VA_DAO
from sasi.habitat.static_grid_model import StaticGridModel
from sasi.fishing.nominal_effort_model import NominalEffortModel

class NominalEffortModelTest(unittest.TestCase):

	def test(self):
		grid_model = StaticGridModel(cell_dao=Test_Cell_DAO()) 
		va = CSV_VA_DAO().load_va()

		effort_model = NominalEffortModel(grid_model=grid_model, va=va)

		cells= grid_model.get_cells()

		efforts = effort_model.get_effort(cells[0], time=1)
		print [e.swept_area for e in efforts]

if __name__ == '__main__':
	unittest.main()
