import unittest

from sasi.dao.habitat.test_habitat_dao import Test_Habitat_DAO
from sasi.habitat.static_grid_habitat_model import StaticGridHabitatModel

class StaticGridHabitatModelTest(unittest.TestCase):

	def test(self):
		habitat_model = StaticGridHabitatModel(habitat_dao=Test_Habitat_DAO()) 

		habitats = habitat_model.get_habitats()

if __name__ == '__main__':
	unittest.main()
