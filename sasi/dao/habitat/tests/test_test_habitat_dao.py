import unittest
from sasi.dao.habitat.test_habitat_dao import Test_Habitat_DAO

class Test_Habitat_DAOTest(unittest.TestCase):

	def test(self):
		habitat_dao = Test_Habitat_DAO()
		habitats = habitat_dao.load_habitats()
		

	def get_session(self):
		return self.session

if __name__ == '__main__':
	unittest.main()
