import unittest
from sasi.sa.tests.basetest import BaseTest
import sasi.sa.metadata as sa_metadata
import sasi.sa.habitat.feature as sa_feature
import sasi.util.habitat.habitat as habitat_util

class FeatureTest(BaseTest):

	def test(self):
		s = self.session
		sa_metadata.metadata.drop_all(s.bind)
		sa_metadata.metadata.create_all(s.bind)

		feature = habitat_util.generate_features(1).pop()
		s.merge(feature)
		s.commit()

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()
	
