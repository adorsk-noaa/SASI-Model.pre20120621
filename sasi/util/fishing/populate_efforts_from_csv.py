import csv
import sasi.conf.conf as conf
import sasi.conf.gear_code_mappings as gear_code_mappings
from sasi.dao.fishing.sa_effort_dao import SA_Effort_DAO
from sasi.dao.habitat.sa_cell_dao import SA_Cell_DAO
import sasi.sa.session as sa_session
from sasi.fishing.effort import Effort
from sasi.fishing.gear import Gear
from sasi.fishing.effort_set import Effort_Set
import sys

def main():

	# Get params from command line.
	if len(sys.argv) != 3:
		print >> sys.stderr, "Must provide csv file and id of effort set to be created in db."
		exit(1)
	csv_file = sys.argv[1]
	tag = sys.argv[2]

	# Setup DAOs.
	db_session = sa_session.get_session()
	effort_dao = SA_Effort_DAO(session = db_session)
	cell_dao = SA_Cell_DAO(session = db_session)

	# Get 100km cells and make id lookup.
	cells = cell_dao.get_cells(filters=[{'attr': 'type', 'op': '==', 'value': 'km100'}])
	cells_by_100km_id = {}
	for c in cells: cells_by_100km_id[c.type_id] = c

	# Make gears lookup.
	gears_by_id = {}
	for gear in db_session.query(Gear).all():
		gears_by_id[gear.id] = gear

	# Create efforts from csv rows.
	efforts = []
	csv_reader = csv.DictReader(open(csv_file, "rb"))
	r_counter = 0
	for r in csv_reader:

		r_counter += 1
		if (r_counter % 1000) == 0:
			print >> sys.stderr, r_counter

		# Get cell.
		cell = cells_by_100km_id[int(r['id_100'])]

		# Get gear.
		gear_id = "GC%s" % r['gear_code']
		gear = gears_by_id[gear_id]

		# Create effort.
		efforts.append(Effort(
			cell = cell,
			time = r['year'],
			gear = gear,
			tag = tag,
			swept_area = float(r['A']),
			hours_fished = float(r['hours_fished'])
			))
	
	# Save efforts.
	effort_dao.save_efforts(efforts)

if __name__ == '__main__': main()
