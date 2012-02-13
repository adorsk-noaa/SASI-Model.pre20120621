import unittest
import sasi.conf.conf as conf
import sasi.util.results.results as results_util

class ResultsUtilTest(unittest.TestCase):

	def test(self):
		result_key = (0, 'km100', 0, 'S1', 'High', 'GC1', 'F1')
		results_util.result_key_to_simid(result_key)

if __name__ == '__main__':
	unittest.main()




