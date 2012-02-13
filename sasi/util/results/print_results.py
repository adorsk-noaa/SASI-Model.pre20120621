import sasi.conf.conf as conf

from sasi.results.sasi_results_model import SASI_Results_Model

import sasi.util.results.results as results_util

def main():
	results = SASI_Results_Model()

	for result_key, value in results.Z.items():

		# Translate key to simid.
		simid = results_util.result_key_to_simid(result_key)

		print simid, value, result_key[0]



if __name__ == '__main__': main()
