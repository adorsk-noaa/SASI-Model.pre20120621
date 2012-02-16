import unittest
import sasi.conf.conf as conf
import sasi.util.results.results as results_util

class Results_Util_Test(unittest.TestCase):

	def test(self):

		sasi_results = results_util.generate_sasi_results(n=10)
		sasi_result_collections = results_util.generate_sasi_result_collections(n=1, results_per_collection=5)	

if __name__ == '__main__':
	unittest.main()




