import sasi.conf.conf as conf
import re

# Converts a result key to a legacy-style simid key
def result_key_to_simid(result_key):

	result_key_parts = result_key.split(',')

	key_parts = {}

	# Format generic key parts.
	key_part_positions = {
			0: 'time',
			2: 'cell_type_id',
			3: 'substrate',
			4: 'energy',
			5: 'gear',
			6: 'feature'
			}

	for pos, part_name in key_part_positions.items():
		key_parts[part_name] = int(float(re.findall(r'(\d+(\.\d+)?)', "%s" % result_key_parts[pos])[0][0]))

	# Generate legacy key from parts.
	simid = key_parts['cell_type_id'] * 1000000000
	simid += key_parts['gear'] * 100000
	simid += key_parts['substrate'] * 1000
	simid += key_parts['energy'] * 100
	simid += key_parts['feature']

	return simid
