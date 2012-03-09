import unittest
from sasi.sa.tests.basetest import BaseTest
from sasi.dao.habitat.sa_habitat_dao import SA_Habitat_DAO

class SA_Habitat_DAOTest(BaseTest):

	def test(self):
		habitat_dao = SA_Habitat_DAO(session=self.session)

		habitats = habitat_dao.get_habitats()
		connection_str = habitat_dao.get_mapserver_connection_string()
		data_str = habitat_dao.get_mapserver_data_string()

	def get_session(self):
		return self.session

if __name__ == '__main__':
	unittest.main()
