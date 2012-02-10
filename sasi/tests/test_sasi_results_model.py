import unittest
from sasi.sasi_results_model import SASI_Results_Model
from sasi.dao.results.pytables_sasi_results_dao import Pytables_SASI_Results_DAO

class SASI_Results_ModelTest(unittest.TestCase):

	def test(self):

		results_dao = Pytables_SASI_Results_DAO(h5file_path='/tmp/test.hd5')

		results_model = SASI_Results_Model(results_dao=results_dao)

		results = []
		for i in range(10):
			result = {
					'result_type': 'X',
					'time': i % 2,
					'cell_id': i,
					'substrate': "S%s" % ((i % 2) + 1),
					'energy': 'High',
					'gear': "G%s" % ((i % 2) + 1),
					'value': i
					}
			results.append(result)

		for result in results:
			results_model.create_result(result)

		for result in results:
			result['value'] *= 10
			results_model.update_result(result)

		old_result = results[0]
		old_result['value'] = 99
		new_result = {
				'result_type': 'Y',
				'time': 0,
				'cell_id': 1000,
				'substrate': 'S10',
				'energy': 'High',
				'gear': 'G1',
				'value': 1000
				}
		results_model.create_or_update_result(old_result)
		results_model.create_or_update_result(new_result)

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()




