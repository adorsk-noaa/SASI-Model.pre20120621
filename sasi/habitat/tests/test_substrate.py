import unittest
from sasi.habitat.substrate import Substrate

class SubtrateTest(unittest.TestCase):

	def test(self):
		s = generate_substrates(1).pop()
		self.failUnless(True)

def generate_substrates(n):
	substrates = []
	for i in range(0,n):
		s = Substrate(n, "substrate-%s" % n)
		substrates.append(s)
	return substrates
		

if __name__ == '__main__':
	unittest.main()




