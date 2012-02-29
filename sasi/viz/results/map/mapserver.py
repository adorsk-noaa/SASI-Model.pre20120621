"""
Functions for creating result maps via MapServer.
"""

import sasi.conf.conf as conf
import sasi.conf.baselayers as baselayers_conf
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('sasi.viz.results.map', 'templates'))

def get_results_map():
	global env

	# Get baselayers.
	base_layers = [getattr(baselayers_conf,layer) for layer in ["coastline", "state_boundaries", "eez", "sasi_domain_boundary"]]

	# Get DB connection string.

	# Get raw SQL query for results.

	# Generate color map.

	# Process mapfile template.

	mapfile_template = env.get_template('results.mapfile.tpl')
	mapfile_content = mapfile_template.render(
		img_width = 200,
		img_height = 200,
		base_layers = base_layers,
		field = "da_field",
		field_data_source = "da field datasource",
		color_classes = []
	)
	print mapfile_content

	# Write processed template to a tmp mapfile.

	# Create map image from template.

	# Remove tmp mapfile.

	# Crop map image.

	# Return image.

