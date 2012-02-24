import sasi.conf.conf as conf
import sasi.conf.fishing as fishing_conf
import sasi.sa.session as sa_session
from sasi.fishing.gear import Gear
import sasi.sa.fishing.gear as sa_gear

def main():

	# Get DB session.
	session = sa_session.get_session()

	# Clear gears table.
	session.execute(sa_gear.table.delete())

	# Create gear object for each gear definition in fishing_conf.
	gear_objs = []
	for gear_definition in fishing_conf.gear_definitions:
		g_obj = Gear(
				id = gear_definition['id'],
				name = gear_definition['name'],
				category = gear_definition['category']
				)
		gear_objs.append(g_obj)

	# Add gear objects to session and save to DB.
	session.add_all(gear_objs)
	session.commit()

if __name__ == '__main__': main()
