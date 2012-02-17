import unittest
from sasi.dao.habitat.test_feature_dao import Test_Feature_DAO

from sasi.habitat.features_model import Features_Model

class Features_Model_Test(unittest.TestCase):

	def test(self):
		features_model = Features_Model(feature_dao=Test_Feature_DAO()) 

		features = features_model.get_features()

if __name__ == '__main__':
	unittest.main()
