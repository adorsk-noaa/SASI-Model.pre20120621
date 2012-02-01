import unittest
from collections import defaultdict
from sasi.habitat.habitat import Habitat

class HabitatTest(unittest.TestCase):

	def test(self):
		h = self.generateHabitats(1).pop()
		print h

		self.failUnless(True)

	def generateHabitats(self,n):
		habitats = []
		for i in range(0,n):
			h = Habitat()
			habitats.append(h)
		return habitats
			

if __name__ == '__main__':
	unittest.main()




