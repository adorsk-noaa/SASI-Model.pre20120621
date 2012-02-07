import unittest
from sasi.dao.va.csv_va_dao import CSV_VA_DAO

class CSV_VA_DAO_Test(unittest.TestCase):

	def test(self):
		va_dao = CSV_VA_DAO()
		va = va_dao.load_va()
		

	def get_session(self):
		return self.session

if __name__ == '__main__':
	unittest.main()
