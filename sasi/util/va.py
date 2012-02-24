import csv
import sasi.conf.conf as conf
import sasi.conf.fishing as fishing_conf

def read_va_from_csv(csv_filename):
	csv_reader = csv.DictReader(open(csv_filename,'rb'))

	# Decorate rows per mappings.
	decorated_rows = []
	for r in csv_reader:

		# Map dry gear codes to categories.
		r['GEAR_CATEGORY'] = fishing_conf.dry_code_to_gear_category.get(r['GEAR_CODE'])

		decorated_rows.append(r)

	return decorated_rows

