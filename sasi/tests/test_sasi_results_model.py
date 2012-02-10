import unittest
from sasi.sasi_results_model import SASI_Results_Model

class SASI_Results_ModelTest(unittest.TestCase):

	def test(self):

		results_model = SASI_Results_Model()

		results = []
		for i in range(10):
			result = {
					'time': i % 2,
					'cell_id': i,
					'substrate': "S%s" % ((i % 2) + 1),
					'energy': 'High',
					'gear': "G%s" % ((i % 2) + 1),
					'value': i
					}
			results.append(result)

		for result in results:
			result_key = ','.join("%s" % s for s in [ result['time'], result['cell_id'], result['substrate'], result['energy'], result['gear'] ])
			results_model.A[result_key] = result['value']
			results_model.A[result_key] += 50

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()




