import sasi.conf.conf as conf
import re
import csv

# Converts a result key to a legacy-style simid key
def result_key_to_simid(result_key):

	# Generic simid parts to be formatted.
	simid_parts = {
			'cell_id': 0,
			'gear': 0,
			'substrate': 0,
			'feature': 0
			}

	# Get result key as dictionary.
	result_key_dict = result_key_to_dict(result_key)

	for part_name in simid_parts.keys():
		simid_parts[part_name] = int(float(re.findall(r'(\d+(\.\d+)?)', "%s" % result_key_dict[part_name])[0][0]))
	
	# Format energy.
	simid_parts['energy'] = 0.0
	if result_key_dict['energy'] == 'High': simid_parts['energy'] = 1.0
	
	# Generate legacy key from parts.
	simid = simid_parts['cell_id'] * 1000000000
	simid += simid_parts['gear'] * 100000
	simid += simid_parts['substrate'] * 1000
	simid += simid_parts['energy'] * 100
	simid += simid_parts['feature']

	return "%d" % simid

def result_key_to_dict(result_key):

	result_key_dict = {}

	result_key_parts = result_key.split(',')

	key_part_positions = {
			0: 'time',
			1: 'cell_id',
			2: 'substrate',
			3: 'energy',
			4: 'gear',
			5: 'feature'
			}

	for pos, part_name in key_part_positions.items():
		result_key_dict[part_name] = result_key_parts[pos]
	
	return result_key_dict


# Print results as csv.
def results_to_csv(results=None):

	# Group results into rows by simid.
	result_rows = {}

	for result_type in ['Z', 'A', 'Y', 'X']:
		type_table = getattr(results, result_type)

		for result_key, value in type_table.items():

			# Get simid.
			simid = result_key_to_simid(result_key)

			row = result_rows.setdefault(simid, {})
			t = result_key[0]
			row["%s_%s" % (result_type, t)] = value

			# Save simid to row.
			row['simid'] = simid

			# Save result key to row.
			row['result_key'] = result_key

	# For each result row... 
	for result_key, row in result_rows.items():

		# Add info columns, except time.
		rk_dict = result_key_to_dict(row['result_key'])
		for k,v in rk_dict.items():
			if not k == 'time':
				row[k] = v

		# Remove result key.
		del row['result_key']

	# Create csv field headers for results.
	fields = result_rows.values()[0].keys()
	fields.sort()
	csv_str = ','.join(fields) + "\n"
	for row in result_rows.values():
		csv_str += ','.join(["%s" % row[f] for f in fields]) + "\n"
	
	return csv_str
