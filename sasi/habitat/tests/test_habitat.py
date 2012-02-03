import unittest
from collections import defaultdict
from sasi.habitat.habitat import Habitat
from sasi.habitat.tests import test_feature
from sasi.habitat.tests import test_substrate
import sasi.tests.geo_util as geo_util

class HabitatTest(unittest.TestCase):

	def test(self):
		h = generate_habitats(1).pop()
		print h
		self.failUnless(True)

def generate_habitats(n):
	habitats = []
	for i in range(0,n):
		id_km100 = "id_km100-%s" % n
		id_km1000 = "id_km1000-%s" % n
		id_vor = "id_vor-%s" % n
		z = n
		substrate = test_substrate.generate_substrates(1).pop()
		energy = n % 2
		features = test_feature.generate_features(2)
		area = n
		geom = geo_util.generate_multipolygon()
		h = Habitat(id_km100, id_km1000, id_vor, z, substrate, energy, features, area, geom)
		habitats.append(h)
	return habitats
		

if __name__ == '__main__':
	unittest.main()




