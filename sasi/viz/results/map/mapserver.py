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

	# Get DB connection string.

	# Get raw SQL query for results.

	# Generate color classes for field.
	color_classes = []
	num_classes = 10
	field_min = 100
	field_max = 200
	field_range = field_max - field_min

	# Define generic color map.
	start_hsv = (0,100,0)
	end_hsv = (0,100,100)
	generic_cm = {'p': [0], 'v': [start_hsv]}
	for n in range(1, num_classes):
		position = 1.0 * n/num_classes
		value = transition3(position, 1.0, start_hsv, end_hsv)
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
	color_classes.append(get_color_class(field=field, cmax=field_cm['p'][0], hsv=field_cm['v'][0]))

	# Create the middle color classes.
	for i in range(1, len(field_cm['p']) - 1):
		color_classes.append(get_color_class(field=field, cmin=field_cm['p'][i], cmax=field_cm['p'][i+1], hsv=field_cm['v'][i+1]))

	# Create the last color class.
	color_classes.append(get_color_class(field=field, cmin=field_cm['p'][-1], hsv=field_cm['v'][-1]))

	print color_classes

	# Process mapfile template.
	field_data_source = """
	CONNECTIONTYPE POSTGIS
	CONNECTION "host=localhost dbname=dev_sasi user=sasi password=sasi port=5432"
	DATA "geom from (select c.geom, c.id as cell_id, sum(r.value) as value from public.result r JOIN public.cell c ON c.id = r.cell_id WHERE r.time = 2009 AND r.tag = 'gc30_all' GROUP BY c.id, r.tag, r.time, c.geom) AS subquery USING UNIQUE cell_id USING srid=4326"
	"""

	mapfile_template = env.get_template('results.mapfile.tpl')
	mapfile_content = mapfile_template.render(
		img_width = 800,
		img_height = 800,
		base_layers = base_layers,
		field = "da_field",
		field_data_source = field_data_source,
		color_classes = []
	)
	#print mapfile_content


	# Write processed template to a tmp mapfile.

	# Create map image from template.

	# Remove tmp mapfile.

	# Crop map image.

	# Return image.

def get_color_class(field=None, cmin=None, cmax=None, hsv=None):

	# Create criteria strings.
	criteria = []
	if cmin: criteria.append({'field': field, 'op': '>=', 'value': cmin})
	if cmax: criteria.append({'field': field, 'op': '<', 'value': cmax})
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

def transition(value, maximum, start_point, end_point):
	return start_point + (end_point - start_point)*value/maximum

def transition3(value, maximum, (s1, s2, s3), (e1, e2, e3)):
	r1= transition(value, maximum, s1, e1)
	r2= transition(value, maximum, s2, e2)
	r3= transition(value, maximum, s3, e3)
	return (r1, r2, r3)


if __name__ == '__main__': main()
