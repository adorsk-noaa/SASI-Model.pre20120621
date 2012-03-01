"""
Functions for creating result maps via MapServer.
"""

import sasi.conf.conf as conf
import sasi.conf.baselayers as baselayers_conf
from jinja2 import Environment, PackageLoader
import colorsys
import bisect

env = Environment(loader=PackageLoader('sasi.viz.results.map', 'templates'))

def main():
	get_results_map()

def get_results_map():
	global env

	# Get baselayers.
	base_layers = [getattr(baselayers_conf,layer) for layer in ["coastline", "state_boundaries", "eez", "sasi_domain_boundary"]]

	field = 'ZZ'
	attr_name = 'value_sum'

	
	#data_str = "geom from (select c.geom, c.id as cell_id, sum(r.value) as %s from public.result r JOIN public.cell c ON c.id = r.cell_id WHERE r.field = '%s' AND r.time = 2010 AND r.tag = 'gc30_all' GROUP BY c.id, r.tag, r.time, c.geom) AS subquery USING UNIQUE cell_id USING srid=4327"
	data_str = "geom from (SELECT sum(anon_1.value) AS value_sum, ST_AsBinary(cell.geom) AS geom, cell.id AS geom_id FROM (SELECT result.time AS time, result.cell_id AS cell_id, result.habitat_type_id AS habitat_type_id, result.gear_id AS gear_id, result.feature_id AS feature_id, result.tag AS tag, result.field AS field, result.value AS value FROM result JOIN cell ON cell.id = result.cell_id JOIN feature ON feature.id = result.feature_id JOIN habitat_type ON habitat_type.id = result.habitat_type_id JOIN substrate ON substrate.id = habitat_type.substrate_id WHERE result.tag = 'gc30_all' AND result.time = 1999 AND cell.type_id = 4119 AND feature.category = '2' AND substrate.id = 'S2' AND field = 'ZZ') AS anon_1 JOIN cell ON cell.id = anon_1.cell_id GROUP BY cell.id) AS subquery USING UNIQUE geom_id USING srid=4326"

	# Get DB connection string.
	field_data_source = """
	CONNECTIONTYPE POSTGIS
	CONNECTION "host=localhost dbname=dev_sasi user=sasi password=sasi port=5432"
	DATA "%s"
	""" % (data_str)


	# Get raw SQL query for results.

	# Generate color classes for field.
	color_classes = []
	num_classes = 10
	field_min = -10.0
	field_max = 0.0
	field_range = field_max - field_min

	# Define generic color map.
	start_hsv = (0.0,0.0,0.0)
	end_hsv = (0.0,0.0,255.0)
	generic_cm = {'p': [0], 'v': [start_hsv]}
	for n in range(1, num_classes):
		position = 1.0 * n/num_classes
		value = interpolate_ntuple(0.0, 1.0, start_hsv, end_hsv, position, 3)
		generic_cm['p'].append(position)
		generic_cm['v'].append(value)

	# Define color map for field. 
	field_cm = {'p': [], 'v': []}
	for n in range(0, num_classes):
		generic_position = 1.0 * n/num_classes 
		field_position = field_min + generic_position * field_range
		cm_index = bisect.bisect_left(generic_cm['p'], generic_position)
		field_value = generic_cm['v'][cm_index]
		field_cm['p'].append(field_position)
		field_cm['v'].append(field_value)

	# Create the first color class.	
	color_classes.append(get_color_class(attr=attr_name, cmax=field_cm['p'][0], hsv=field_cm['v'][0]))

	# Create the middle color classes.
	for i in range(1, len(field_cm['p']) - 1):
		color_classes.append(get_color_class(attr=attr_name, cmin=field_cm['p'][i], cmax=field_cm['p'][i+1], hsv=field_cm['v'][i+1]))

	# Create the last color class.
	color_classes.append(get_color_class(attr_name, cmin=field_cm['p'][-1], hsv=field_cm['v'][-1]))

	# Process mapfile template.
	mapfile_template = env.get_template('results.mapfile.tpl')
	mapfile_content = mapfile_template.render(
		img_width = 800,
		img_height = 800,
		base_layers = base_layers,
		field = field,
		field_data_source = field_data_source,
		color_classes = color_classes
	)
	print mapfile_content


	# Write processed template to a tmp mapfile.

	# Create map image from template.

	# Remove tmp mapfile.

	# Crop map image.

	# Return image.

def get_color_class(attr=None, cmin=None, cmax=None, hsv=None):

	# Create criteria strings.
	criteria = []
	if cmin: criteria.append({'attr': attr, 'op': '>=', 'value': cmin})
	if cmax: criteria.append({'attr': attr, 'op': '<', 'value': cmax})
	criteria_strings = [env.get_template('criterion.tpl').render(criterion=criterion) for criterion in criteria]

	# Set rgb value.
	rgb = colorsys.hsv_to_rgb(*hsv)

	# Return assembled color class.
	return {
		'criteria': criteria_strings,
		'r': rgb[0],
		'g': rgb[1],
		'b': rgb[2]
	}

def interpolate(start_x, end_x, start_y, end_y, x):
	x_range = end_x - start_x
	y_range = end_y - start_y
	return start_y + (x - start_x)/x_range * y_range

def interpolate_ntuple(start_x, end_x, start_y, end_y, x, n):
	return tuple([interpolate(start_x, end_x, start_y[i], end_y[i], x)  for i in range(n)])

if __name__ == '__main__': main()
