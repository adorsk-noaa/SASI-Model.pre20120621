import unittest
from sasi.dao.habitat.test_feature_dao import Test_Feature_DAO

class Test_Feature_DAO_Test(unittest.TestCase):

	def test(self):
		feature_dao = Test_Feature_DAO()
		features = feature_dao.get_features()

	def get_session(self):
		return self.session

if __name__ == '__main__':
	unittest.main()
