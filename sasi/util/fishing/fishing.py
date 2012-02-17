from sasi.fishing.gear import Gear
import sasi.conf.conf as conf
import sasi.util.registry as util_registry

# Gear registry for generated gears.
generated_gears = {}

def generate_gears():

	gears = []

	for i in range(1,6+1):

		o = Gear(
				id = "G%s" % i,
				name = "Gear %s" % i
				)

		gears.append(util_registry.get_or_register_object(o))
	
	return gears
