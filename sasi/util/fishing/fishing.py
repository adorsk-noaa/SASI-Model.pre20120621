from sasi.fishing.gear import Gear
import sasi.conf.conf as conf

def generate_gears():

	gears = []

	for i in range(1,6+1):
		g = Gear(
				id = "G%s" % i,
				name = "Gear %s" % i
				)

		gears.append(g)
	
	return gears
