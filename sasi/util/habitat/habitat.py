from sasi.habitat.habitat_type import Habitat_Type
from sasi.habitat.habitat import Habitat
from sasi.habitat.feature import Feature
from sasi.habitat.substrate import Substrate
from sasi.habitat.cell import Cell
import sasi.conf.conf as conf
import sasi.conf.substrate_mappings as substrate_mappings
import sasi.conf.energy_mappings as energy_mappings
import sasi.util.geo_util as geo_util

def generate_substrates(n):
	substrates = []

	for i in range(n):
		s = Substrate(
				id = n,
				name = "S%s" % i
				)
		substrates.append(s)
	
	return substrates


def generate_features(n):

	features = []

	for i in range(n):
		f = Feature(
				id = n,
				name = "F%s" % i
				)
		features.append(f)
	
	return features

def generate_habitat_types():

	habitat_types = []

	valid_habitat_types = [
			('S5', 'High'),
			('S2', 'Low'),
			('S4', 'Low'),
			('S3', 'Low'),
			('S1', 'Low'),
			('S2', 'High'),
			('S5', 'Low'),
			('S1', 'High'),
			('S3', 'High'),
			('S4', 'High')
			]

	for valid_habitat_type in valid_habitat_types:

		substrate_id = valid_habitat_type[0]
		energy = valid_habitat_type[1]

		substrate = Substrate(id=substrate_id, name=substrate_id)

		ht = Habitat_Type(
				energy = energy,
				substrate = substrate,
				)

		habitat_types.append(ht)

	return habitat_types

def generate_habitats(n, default_area = lambda: 1.0, habitat_types=None):

	habitats= []

	# Generate habitat types if none were given.
	if not habitat_types:
		habitat_types = generate_habitat_types()

	for i in range(n):
		habitat_type = habitat_types[i % len(habitat_types)]
		r = Habitat(
				id = i,
				habitat_type = habitat_type,
				z = i * 100,
				area = default_area(),
				geom = geo_util.generate_multipolygon(),
				)
		habitats.append(r)

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
