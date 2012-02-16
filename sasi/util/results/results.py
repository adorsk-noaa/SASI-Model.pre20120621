import sasi.conf.conf as conf
import sasi.util.habitat.habitat as habitat_util
import sasi.util.fishing.fishing as fishing_util

from sasi.results.sasi_result import SASI_Result
from sasi.results.sasi_result_collection import SASI_Result_Collection

# Generate SASI Results.
def generate_sasi_results(n=10):

	sasi_results = []

	# Get gears.
	gears = fishing_util.generate_gears()

	# Get features.
	features = habitat_util.generate_features(n)

	# Get cells.
	cells = habitat_util.generate_cells(n/2)

	for i in range(n):
		cell_i = cells[i % len(cells)]
		gear_i = gears[i % len(gears)]
		feature_i = features[i % len(features)]
		sasi_result = SASI_Result(
				time = i,
				cell = cell_i,
				habitat_type = cell_i.habitats[0].habitat_type,
				gear = gear_i,
				feature = feature_i,
				field = "field_%s" % i,
				value = i
				)
		sasi_results.append(sasi_result)
	return sasi_results


# Generate SASI Result Collections.
def generate_sasi_result_collections(n=1, results_per_collection=10):
	sasi_result_collections = []

	for i in range(n):
		sasi_results = generate_sasi_results(results_per_collection)
		sasi_result_collection = SASI_Result_Collection(
				id = "sasi_result_collection_%s" % i,
				results = sasi_results
				)
		sasi_result_collections.append(sasi_result_collection)

	return sasi_result_collections


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
def results_to_csv_buffer(results=None, buffer=None):

	# Group results into rows by simid.
	result_rows = {}

	# Fields to output.
	fields = set()

	for result_type in ['Z', 'A', 'Y', 'X']:
		type_table = getattr(results, result_type)

		for result_key, value in type_table.items():

			# Get simid.
			simid = result_key_to_simid(result_key)

			row = result_rows.setdefault(simid, {})
			t = result_key[0]

			# Format the field for this result.
			result_field = "%s_%s" % (result_type, t)
			fields.add(result_field)

			row[result_field] = value

			# Save simid to row.
			row['simid'] = simid
			fields.add('simid')

			# Save result key to row.
			# Note: we don't put out the result_key, so we don't add it to fields.
			row['result_key'] = result_key

	# For each result row... 
	for result_key, row in result_rows.items():

		# Add info columns, except time.
		rk_dict = result_key_to_dict(row['result_key'])
		for k,v in rk_dict.items():
			if not k == 'time':
				row[k] = v
				fields.add(k)

		# Remove result key.
		del row['result_key']

	# Create csv field headers for results.
	fields = list(fields)
	fields.sort()
	print >> buffer, ','.join(fields)
	for row in result_rows.values():
		print >> buffer, ','.join(["%s" % row.get(f,'') for f in fields])
	
