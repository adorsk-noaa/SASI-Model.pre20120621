import sasi.conf.conf as conf
from sasi.va.va import VulnerabilityAssessment
import sasi.util.va as va_util
import sasi.sa.session as sa_session
from sasi.fishing.gear import Gear
import sasi.sa.fishing.gear as sa_gear

def main():

	# Read gears from vulernability assessment.
	va_rows = va_util.read_va_from_csv(conf.conf['va_file'])
	va = VulnerabilityAssessment(rows = va_rows)	
	gears = va.get_gears()

	# Get DB session.
	session = sa_session.get_session()

	# Clear gears table.
	session.execute(sa_gear.table.delete())

	# Create Gear objects
	# note: might move this into the VA object itself later.
	gear_objs = []
	for g in gears.values():
		g_obj = Gear(
				name = g['GEAR'],
				id = g['GEAR_CODE']
				)
		gear_objs.append(g_obj)

	# Add gear objects to session and save to DB.
	session.add_all(gear_objs)
	session.commit()


if __name__ == '__main__': main()
