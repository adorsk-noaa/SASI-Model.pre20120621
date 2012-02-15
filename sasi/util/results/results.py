import sasi.conf.conf as conf
import re
import csv

# Converts a result key to a legacy-style simid key
def result_key_to_simid(result_key):

	result_key_parts = result_key.split(',')

	key_parts = {}

	# Format generic key parts.
	key_part_positions = {
			0: 'time',
			1: 'cell_id',
			2: 'substrate',
			4: 'gear',
			5: 'feature'
			}

	for pos, part_name in key_part_positions.items():
		key_parts[part_name] = int(float(re.findall(r'(\d+(\.\d+)?)', "%s" % result_key_parts[pos])[0][0]))
	
	# Format energy.
	key_parts['energy'] = 0.0
	if result_key_parts[4] == 'High': key_parts['energy'] = 1.0

	# Generate legacy key from parts.
	simid = key_parts['cell_id'] * 1000000000
	simid += key_parts['gear'] * 100000
	simid += key_parts['substrate'] * 1000
	simid += key_parts['energy'] * 100
	simid += key_parts['feature']

	return "%s" % simid

# Print results as csv.
def results_to_csv(results=None):

	# Group results by simid.
	grouped_results = {}

	for result_type in ['Z', 'A', 'Y', 'X']:
		type_table = getattr(results, result_type)

		for result_key, value in type_table.items():

			# Translate key to simid.
			simid = result_key_to_simid(result_key)

			simid_results = grouped_results.setdefault(simid, {})
			t = result_key[0]
			simid_results["%s_%s" % (result_type, t)] = value

	simids = grouped_results.keys()
	simids.sort()

	result_keys = grouped_results[simids[0]].keys()
	result_keys.sort()
	result_keys = ['simid'] + result_keys

	csv_str = ','.join(result_keys) + "\n"
	for s in simids:
		csv_str += ','.join([s] + ["%s" % grouped_results[s][rk] for rk in result_keys[1:]]) + "\n"
	
	return csv_str
