import unittest
from collections import defaultdict
from sasi.habitat.feature import Feature

class FeatureTest(unittest.TestCase):

	def test(self):
		f = generate_features(1).pop()

		self.failUnless(True)

def generate_features(n):
	features = []
	for i in range(0,n):
		f = Feature("feature %s" % n, n, n % 2)
		features.append(f)
	return features
		

if __name__ == '__main__':
	unittest.main()




