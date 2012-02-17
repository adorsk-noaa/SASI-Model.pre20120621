from sasi.fishing.gear import Gear
import sasi.conf.conf as conf

# Gear registry for generated gears.
generated_gears = {}

def generate_gears():

	gears = []

	for i in range(1,6+1):

		g = Gear(
				id = "G%s" % i,
				name = "Gear %s" % i
				)

		if not generated_gears.has_key(g.id):
			generated_gears[g.id] = g

		gears.append(generated_gears[g.id])
	
	return gears
