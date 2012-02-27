import sasi.conf.conf as conf
import sasi.util.habitat.habitat as habitat_util
import sasi.util.fishing.fishing as fishing_util
import sasi.util.registry as util_registry

from sasi.results.result import Result
from sasi.results.result_set import Result_Set

generated_results = {}
generated_result_sets = {}

# Generate Results.
def generate_results(n=10, tags=["a", "b"]):

	results = []

	# Get gears.
	gears = fishing_util.generate_gears()

	# Get features.
	features = habitat_util.generate_features(n)

	# Get cells.
	cells = habitat_util.generate_cells(n/2 + 1)

	for i in range(n):
		cell_i = cells[i % len(cells)]
		gear_i = gears[i % len(gears)]
		feature_i = features[i % len(features)]
		o = Result(
				time = i,
				cell = cell_i,
				habitat_type = cell_i.habitats[0].habitat_type,
				gear = gear_i,
				feature = feature_i,
				field = "field_%s" % i,
				tag = tags[i % len(tags)],
				value = i
				)

		results.append(util_registry.get_or_register_object(o,id_func=lambda obj: id(obj)))

	return results

