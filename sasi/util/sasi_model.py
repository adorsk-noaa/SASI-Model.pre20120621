import sasi.conf.conf as conf
import sasi.conf.fishing as fishing_conf
import re
from sasi.habitat.cell import Cell
from sasi.habitat.feature import Feature
from sasi.habitat.substrate import Substrate
from sasi.habitat.habitat_type import Habitat_Type
from sasi.fishing.gear import Gear

from sasi.results.result import Result
from sasi.results.result_set import Result_Set

# Converts a result key to a legacy-style simid key
def result_key_to_simid(result_key):

	# Generic simid parts to be formatted.
	simid_parts = {
			'cell_id': 0,
			'substrate': 0,
			'feature': 0,
			'gear_dry_code': 0
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
	simid += simid_parts['gear_dry_code'] * 100000
	simid += simid_parts['substrate'] * 1000
	simid += simid_parts['energy'] * 100
	simid += simid_parts['feature']

	return "%d" % simid

def result_key_to_dict(result_key):

	result_key_dict = {
			'time': result_key[0],
			'cell_id': result_key[1].id,
			'cell_type': result_key[1].type,
			'cell_type_id': result_key[1].type_id,
			'substrate': result_key[2].substrate.id,
			'energy': result_key[2].energy,
			'gear_dry_code': fishing_conf.gear_category_to_dry_code[result_key[3].category],
			'feature': result_key[4].id
			}

	return result_key_dict


# Print results as csv.
def results_to_csv_buffer(results=None, buffer=None):

	# Group results into rows by simid.
	result_rows = {}

	# Fields to output.
	fields = set()

	for c in results.keys():
		for t in results[c].keys():
			for result_field in results[c][t].keys():
				field_results = results[c][t][result_field]

				for result_key, value in field_results.items():

					# Get simid.
					simid = result_key_to_simid(result_key)

					row = result_rows.setdefault(simid, {})
					t = result_key[0]

					# Format the field for this result.
					field_time = "%s_%s" % (result_field, t)
					row[field_time] = value
					fields.add(field_time)

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
	

# Create Result Set from results.
def results_to_result_set(results=None):

	result_objects = []

	# For each result...
	for c in results.keys():
		for t in results[c].keys():
			for result_field in results[c][t].keys():

				# Get results for that field.
				field_results = results[c][t][result_field]

				# For each result...
				for result_key, field_value in field_results.items():

					# Create SASI_Result object w/ minimal stub objects as attributes.
					result_object = Result(
							time = result_key[0],
							cell = result_key[1],
							habitat_type = result_key[2],
							gear = result_key[3],
							feature = result_key[4],
							field = result_field,
							value = field_value
							)
					result_objects.append(result_object)
			
	return Result_Set(results = result_objects)




