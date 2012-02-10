import unittest

from sasi.dao.results.pytables_sasi_results_dao import Pytables_SASI_Results_DAO

class Pytables_SASI_Results_DAO_Test(unittest.TestCase):

	def test(self):
		test_file = '/tmp/test.hd5'

		results_dao = Pytables_SASI_Results_DAO(h5file_path = test_file)

		results = []
		for i in range(10):
			result = {
					'result_type': 'X',
					'time': i % 2,
					'substrate': "S%s" % ((i % 2) + 1),
					'energy': 'High',
					'gear': "G%s" % ((i % 2) + 1),
					'value': i
					}
			results.append(result)

		results_dao.create_results(results)

		fetched_results = results_dao.get_results(
				filters=[
					{
						'name': 'time',
						'operator': '==',
						'values': [1],
						}
				],
				as_proxy=False
				)

		for r in results:
			r['value'] = r['value'] * 10

		results_dao.update_results(results)
			
		fetched_results = results_dao.get_results(as_proxy=False)

if __name__ == '__main__':
	unittest.main()
