import unittest
from sasi.sa.tests.basetest import BaseTest
from sasi.dao.habitat.sa_feature_dao import SA_Feature_DAO

class SA_Feature_DAO_Test(BaseTest):

	def test(self):
		feature_dao = SA_Feature_DAO(session=self.session)
		features = feature_dao.get_features()

	def get_session(self):
		return self.session

if __name__ == '__main__':
	unittest.main()
