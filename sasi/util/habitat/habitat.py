from sasi.habitat.habitat import Habitat
from sasi.habitat.feature import Feature
from sasi.habitat.substrate import Substrate
from sasi.habitat.cell import Cell
import sasi.conf.conf as conf
import sasi.conf.feature_assignments as feature_assignments
import sasi.conf.substrate_mappings as substrate_mappings
import sasi.conf.energy_mappings as energy_mappings
import sasi.tests.geo_util as geo_util

def generate_habitats(n, default_area = lambda: 1):

	valid_habitats = [('S5', '1.0'), ('S2', '0.0'), ('S4', '0.0'), ('S3', '0.0'), ('S1', '0.0'), ('S2', '1.0'), ('S5', '0.0'), ('S1', '1.0'), ('S3', '1.0'), ('S4', '1.0')]

	habitats = []
	for i in range(n):

		habitat_type = valid_habitats[i % len(valid_habitats)]
		
		substrate_id = habitat_type[0]
		energy = habitat_type[1]

		substrate = Substrate(id=substrate_id, name=substrate_id)

		assignments = feature_assignments.assignments[(substrate_id, energy)]
		features = [Feature(id=a,name=a) for a in assignments]

		h = Habitat(
				id = i,
				id_km100 = i,
				id_km1000 = i,
				id_vor = i,
				z = i * -1.0,
				energy = energy,
				substrate = substrate,
				features = features,
				area = default_area(),
				geom = geo_util.generate_multipolygon(),
				)

		habitats.append(h)

	return habitats


def generate_cells(n, default_area = lambda: 1.0, habitats=None, habitats_per_cell=2):

	cells = []

	# Generate habitats if none were given.
	if not habitats:
		default_habitat_area = lambda: 1.0 * default_area()/habitats_per_cell 
		habitats = generate_habitats(n * habitats_per_cell, default_area = default_habitat_area)

	for i in range(n):

		cell_habitats = [habitats.pop() for i in range(habitats_per_cell)]

		c = Cell(
				id = i,
				area = default_area(),
				geom = geo_util.generate_multipolygon(),
				habitats = cell_habitats
				)

		cells.append(c)

	return cells
