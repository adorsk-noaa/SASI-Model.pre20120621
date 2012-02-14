import sasi.conf.conf as conf

from sasi.results.sasi_results_model import SASI_Results_Model

import sasi.util.results.results as results_util

import csv

def main():
	results = SASI_Results_Model()

	# Group results by simid.
	grouped_results = {}

	for result_type in ['Z', 'A', 'Y', 'X']:
		type_table = getattr(results, result_type)

		for result_key, value in type_table.items():

			# Translate key to simid.
			simid = results_util.result_key_to_simid(result_key)

			simid_results = grouped_results.setdefault(simid, {})
			t = result_key[0]
			simid_results["%s_%s" % (result_type, t)] = value

	simids = grouped_results.keys()
	simids.sort()

	result_keys = grouped_results[simids[0]].keys()
	result_keys.sort()
	result_keys = ['simid'] + result_keys

	print ','.join(result_keys)
	for s in simids:
		print ','.join([s] + ["%s" % grouped_results[s][rk] for rk in result_keys[1:]])
	

if __name__ == '__main__': main()
