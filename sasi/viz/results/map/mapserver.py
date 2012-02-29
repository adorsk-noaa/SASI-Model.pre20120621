"""
Functions for creating result maps via MapServer.
"""

import sasi.conf.conf as conf
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('sasi.viz.results.map', 'templates'))

def get_results_map():
	global env

	# Get DB connection string.

	# Get raw SQL query for results.

	# Generate color map.

	# Process mapfile template.

	# Write processed template to a tmp mapfile.

	# Create map image from template.

	# Remove tmp mapfile.

	# Crop map image.

	# Return image.

