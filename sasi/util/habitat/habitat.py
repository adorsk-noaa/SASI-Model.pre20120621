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
	energy_codes = list(set(energy_mappings.shp_to_va.values()))

	substrate_codes = list(set(substrate_mappings.shp_to_va.values()))

	habitats = []
	for i in range(n):
		energy = energy_codes[i % len(energy_codes)]
		
		substrate_id = substrate_codes[i % len(substrate_codes)]
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
