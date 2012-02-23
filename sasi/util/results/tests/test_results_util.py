import unittest
import sasi.conf.conf as conf
import sasi.util.results.results as results_util

class Results_Util_Test(unittest.TestCase):

	def test(self):

		results = results_util.generate_results(n=10)
		result_sets =results_util.generate_result_sets(n=1, results_per_collection=5)	

if __name__ == '__main__':
	unittest.main()




