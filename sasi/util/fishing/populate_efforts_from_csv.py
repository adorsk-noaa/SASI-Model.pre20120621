import csv
import sasi.conf.conf as conf
from sasi.dao.fishing.sa_effort_dao import SA_Effort_DAO
from sasi.dao.habitat.sa_cell_dao import SA_Cell_DAO
import sasi.sa.session as sa_session
from sasi.fishing.effort import Effort
from sasi.fishing.effort_set import Effort_Set
import sys

def main():

	# Get params from command line.
	if len(sys.argv) != 3:
		print >> sys.stderr, "Must provide csv file and id of effort set to be created in db."
		exit(1)
	csv_file = sys.argv[1]
	effort_set_id = sys.argv[2]

	# Setup DAOs.
	db_session = sa_session.get_session()
	effort_dao = SA_Effort_DAO(session = db_session)
	cell_dao = SA_Cell_DAO(session = db_session, default_filters=[{'attr': 'type', 'op': '==', 'value': 'km100'}])

	# Create efforts from csv rows.
	efforts = []
	csv_reader = csv.DictReader(open(csv_file, "rb"))
	for r in csv_reader:

		# Get cell.
		cell = cell_dao.get_cells(filters=[{'attr': 'type_id', 'op': '==', 'value': r['id_100']}])

		# Get gear.
		gear

		# Get gear.
		efforts.append(Effort(
			cell = c,
			time = r['year'],
			gear = g,
			swept_area = float(r['A']),
			hours_fished = float(r['hours_fished'])
			))
		{'A': '0.00732691518963', 'gear_code': '50', 'hours_fished': '53.7511902667856', '_FREQ_': '2', 'id_100': '741', '_TYPE_': '0', 'value': '1114.22815351244', 'year': '1998'}

	

if __name__ == '__main__': main()
