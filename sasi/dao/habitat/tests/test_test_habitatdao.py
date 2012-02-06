import unittest
from sasi.dao.habitat.test_habitatdao import Test_HabitatDAO

class Test_HabitatDAOTest(unittest.TestCase):

	def test(self):
		habitat_dao = Test_HabitatDAO()
		habitats = habitat_dao.load_habitats()
		

	def get_session(self):
		return self.session

if __name__ == '__main__':
	unittest.main()
