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
	field_data_source = """
CONNECTIONTYPE POSTGIS
CONNECTION "host=localhost dbname=dev_sasi user=sasi password=sasi port=5432"
DATA "geom from 
(
select c.geom, c.type_id, sum(r.value) as value
from public.result r JOIN public.cell c ON c.type_id = r.cell_type_id AND c.type = r.cell_type
WHERE c.type = 'km100' AND r.time = 5 
GROUP BY c.type_id, r.time
) AS subquery USING UNIQUE type_id"
	"""

	mapfile_template = env.get_template('results.mapfile.tpl')
	mapfile_content = mapfile_template.render(
		img_width = 200,
		img_height = 200,
		base_layers = base_layers,
		field = "da_field",
		field_data_source = field_data_source,
		color_classes = []
	)
	print mapfile_content

	# Write processed template to a tmp mapfile.

	# Create map image from template.

	# Remove tmp mapfile.

	# Crop map image.

	# Return image.

