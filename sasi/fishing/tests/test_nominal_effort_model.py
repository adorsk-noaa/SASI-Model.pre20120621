import unittest

from sasi.dao.habitat.test_habitat_dao import Test_Habitat_DAO
from sasi.dao.va.csv_va_dao import CSV_VA_DAO
from sasi.habitat.static_grid_habitat_model import StaticGridHabitatModel
from sasi.fishing.nominal_effort_model import NominalEffortModel

class NominalEffortModelTest(unittest.TestCase):

	def test(self):
		habitat_model = StaticGridHabitatModel(habitat_dao=Test_Habitat_DAO()) 
		va = CSV_VA_DAO().load_va()

		effort_model = NominalEffortModel(habitat_model=habitat_model, va=va)

		habitats = habitat_model.get_habitats()
		cells = list(set([h.id_km100 for h in habitats]))

		efforts = effort_model.get_effort(cells[0], time=1)
		print [e.swept_area for e in efforts]

if __name__ == '__main__':
	unittest.main()
