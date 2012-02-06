import unittest
from sasi.sa.tests.basetest import BaseTest
import sasi.sa.habitat.feature as sa_feature
from sasi.habitat.feature import Feature
import sasi.habitat.tests.test_feature as test_feature

class FeatureTest(BaseTest):

	def test(self):
		features = test_feature.generate_features(1)
		s = self.session
		sa_feature.metadata.create_all(s.bind)
		s.add_all(features)
		s.commit()
		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()
	
