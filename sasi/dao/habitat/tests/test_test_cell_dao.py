import unittest
from sasi.dao.habitat.test_cell_dao import Test_Cell_DAO

class Test_Cell_DAOTest(unittest.TestCase):

	def test(self):
		cell_dao = Test_Cell_DAO()
		cells = cell_dao.get_cells()
		print cells

	def get_session(self):
		return self.session

if __name__ == '__main__':
	unittest.main()
