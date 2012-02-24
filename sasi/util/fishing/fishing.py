from sasi.fishing.gear import Gear
import sasi.conf.conf as conf
import sasi.conf.fishing as fishing_conf
import sasi.util.registry as util_registry
from sasi.fishing.effort import Effort
from sasi.fishing.effort_set import Effort_Set
import sasi.util.habitat.habitat as habitat_util

# Gear registry for generated gears.
generated_gears = {}

def generate_gears():

	# Create gear object for each gear definition in fishing_conf.
	gears = []
	for gear_definition in fishing_conf.gear_definitions:
		o = Gear(
				id = gear_definition['id'],
				name = gear_definition['name'],
				category = gear_definition['category']
				)

		gears.append(util_registry.get_or_register_object(o))
	
	return gears

# Generate Efforts.
def generate_efforts(n=10, times=[1,2], default_swept_area=lambda: 1, default_hours_fished=lambda: 1):

	efforts = []

	# Get gears.
	gears = generate_gears()

	# Get cells.
	cells = habitat_util.generate_cells(n/2 + 1)

	for i in range(n):
		cell_i = cells[i % len(cells)]
		gear_i = gears[i % len(gears)]
		time = times[i % len(times)]
		o = Effort(
				cell = cell_i,
				time = time,
				gear = gear_i,
				swept_area = default_swept_area(),
				hours_fished = default_hours_fished() 
				)

		efforts.append(util_registry.get_or_register_object(o,id_func=lambda obj: id(obj)))

	return efforts

# Generate Effort Sets.
def generate_effort_sets(n=1, efforts_per_set=10):
	effort_sets = []

	for i in range(n):
		efforts = generate_efforts(efforts_per_set)
		o = Effort_Set(
				id = "effort_set_%s" % i,
				efforts = efforts
				)

		effort_sets.append(util_registry.get_or_register_object(o))

	return effort_sets

