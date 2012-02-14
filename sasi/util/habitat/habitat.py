from sasi.habitat.habitat import Habitat
from sasi.habitat.feature import Feature
from sasi.habitat.substrate import Substrate
from sasi.habitat.region import Region
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

def generate_habitats():

	habitats = []

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

	for habitat_type in valid_habitat_types:

		substrate_id = habitat_type[0]
		energy = habitat_type[1]

		substrate = Substrate(id=substrate_id, name=substrate_id)

		h = Habitat(
				energy = energy,
				substrate = substrate,
				)

		habitats.append(h)

	return habitats

def generate_regions(n, default_area = lambda: 1.0, habitats=None):

	regions = []

	# Generate habitats if none were given.
	if not habitats:
		habitats = generate_habitats()

	for i in range(n):
		habitat = habitats[i % len(habitats)]
		r = Region(
				id = i,
				habitat = habitat,
				z = i * 100,
				area = default_area(),
				geom = geo_util.generate_multipolygon(),
				)
		regions.append(r)

	return regions


def generate_cells(n, default_area = lambda: 1.0, regions=None, regions_per_cell=2):

	cells = []

	# Generate regions if none were given.
	if not regions:
		default_region_area = lambda: 1.0 * default_area()/regions_per_cell 
		regions = generate_regions(n * regions_per_cell, default_area = default_region_area)

	for i in range(n):

		cell_regions = [regions.pop() for i in range(regions_per_cell)]

		c = Cell(
				id = i,
				area = default_area(),
				geom = geo_util.generate_multipolygon(),
				regions = cell_regions
				)

		cells.append(c)

	return cells
