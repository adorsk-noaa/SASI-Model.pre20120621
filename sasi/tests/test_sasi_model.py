import unittest
from collections import defaultdict
from sasi.sasi_model import SASIModel

class SASIModelTest(unittest.TestCase):

	def test(self):
		"""
		m = SASIModel()
		m.t0 = 0
		m.tf = 2

		m.habitats = [0,1]

		def constant_tau(): return 1.0
		def constant_omega(): return 1.0

		m.tau = defaultdict(constant_tau)
		m.omega = defaultdict(constant_omega)

		for t in range(m.t0, m.tf, m.dt):
			m.iterate(t)
		"""

		self.failUnless(True)


if __name__ == '__main__':
	unittest.main()




