import unittest
from sasi.sa.tests.basetest import BaseTest
from sasi.dao.habitat.sa_cell_dao import SA_Cell_DAO

class SA_Cell_DAOTest(BaseTest):

	def test(self):
		cell_dao = SA_Cell_DAO()
		cell_dao.get_session = self.get_session

		cells = cell_dao.get_cells()

	def get_session(self):
		return self.session

if __name__ == '__main__':
	unittest.main()
