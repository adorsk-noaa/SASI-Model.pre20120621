import unittest
from collections import defaultdict
from sasi.habitat.feature import Feature

class FeatureTest(unittest.TestCase):

	def test(self):
		f = self.generateFeatures(1).pop()
		print f

		self.failUnless(True)

	def generateFeatures(self,n):
		features = []
		for i in range(0,n):
			f = Feature()
			features.append(f)
		return features
			

if __name__ == '__main__':
	unittest.main()




