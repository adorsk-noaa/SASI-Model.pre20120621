import csv

def read_va_from_csv(csv_filename):
	csv_reader = csv.DictReader(open(csv_filename,'rb'))
	return [r for r in csv_reader]
