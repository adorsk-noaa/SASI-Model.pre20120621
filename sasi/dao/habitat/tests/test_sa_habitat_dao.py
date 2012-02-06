import unittest
from sasi.sa.tests.basetest import BaseTest
from sasi.dao.habitat.sa_habitat_dao import SA_HabitatDAO

class SA_HabitatDAOTest(BaseTest):

	def test(self):
		habitat_dao = SA_HabitatDAO()
		habitat_dao.get_session = self.get_session

		habitats = habitat_dao.load_habitats()
		

	def get_session(self):
		return self.session

if __name__ == '__main__':
	unittest.main()
