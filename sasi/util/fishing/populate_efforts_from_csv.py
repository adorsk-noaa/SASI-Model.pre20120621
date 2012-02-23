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
	effort_set_id = sys.argv[2]

	# Setup DAOs.
	db_session = sa_session.get_session()
	effort_dao = SA_Effort_DAO(session = db_session)
	cell_dao = SA_Cell_DAO(session = db_session)

	# Get 100km cells and make id lookup.
	cells = cell_dao.get_cells(filters=[{'attr': 'type', 'op': '==', 'value': 'km100'}])
	cells_by_100km_id = {}
	for c in cells: cells_by_100km_id[c.type_id] = c

	# Make gears lookup.
	gears_by_dry_code = {}
	for wet_code, dry_code in gear_code_mappings.wet_to_dry.items():
		 gear = db_session.query(Gear).filter(Gear.id == dry_code).one()
		 gears_by_dry_code[dry_code] = gear

	# Create efforts from csv rows.
	efforts = []
	csv_reader = csv.DictReader(open(csv_file, "rb"))
	r_counter = 0
	for r in csv_reader:

		r_counter += 1
		if (r_counter % 1000) == 0:
			print >> sys.stderr, r_counter

		# Get cell.
		cell = cells_by_100km_id[r['id_100']]

		# Get gear.
		wet_code = "GC%s" % r['gear_code']
		dry_code = gear_code_mappings.wet_to_dry[wet_code]
		gear = gears_by_dry_code[dry_code]

		# Create effort.
		efforts.append(Effort(
			cell = cell,
			time = r['year'],
			gear = gear,
			swept_area = float(r['A']),
			hours_fished = float(r['hours_fished'])
			))
	
	# Create effort set from efforts.
	effort_set = Effort_Set(id=effort_set_id, efforts=efforts)

	# Save effort set.
	effort_dao.save_effort_sets(effort_sets=[effort_set])

if __name__ == '__main__': main()
