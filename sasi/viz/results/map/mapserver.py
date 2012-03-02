"""
Functions for creating result maps via MapServer.
"""

import sasi.conf.conf as conf
import sasi.conf.baselayers as baselayers_conf
import sasi.sa.session as sa_session
from sasi.dao.results.sa_result_dao import SA_Result_DAO

from jinja2 import Environment, PackageLoader
import colorsys
import bisect
import os
from PIL import Image
from cStringIO import StringIO
import mapscript

env = Environment(loader=PackageLoader('sasi.viz.results.map', 'templates'))

def main():

	db_session = sa_session.get_session()
	result_dao = SA_Result_DAO(session=db_session)

	filters = [
			{'attr': 'tag', 'op': '==', 'value': 'gc30_all'},
			{'attr': 'Cell.type', 'op': '==', 'value': 'km100'},
			{'attr': 'field', 'op': '==', 'value': 'ZZ'},
			{'attr': 'time', 'op': '==', 'value': 1999},
			]

	get_results_map(result_dao = result_dao, filters=filters)

def get_results_map(result_dao=None, filters=None, colormap=None):
	global env

	# Get baselayers.
	base_layers = [getattr(baselayers_conf,layer) for layer in ["coastline", "state_boundaries", "eez"]]


	# Get DB connection strings.
	connection_str = result_dao.get_mapserver_connection_string()
	data_str = result_dao.get_mapserver_data_string(filters=filters)

	# Assemble data source.
	field_data_source = """
	CONNECTIONTYPE POSTGIS
	CONNECTION "%s"
	DATA "%s"
	""" % (connection_str, data_str)

	# Get field stats.
	stats_row = result_dao.get_field_stats(filters=filters).pop()
	field_stats = dict(zip(stats_row.keys(), stats_row))

	# If no color map was given, get the default color map.
	if not colormap: colormap = get_default_colormap()

	# Generate color classes for field.
	num_classes = 10
	value_min = field_stats['value_min']
	value_max = field_stats['value_max']
	value_range = value_max - value_min

	# Use value_sum as the attr name to match up with data_str.
	attr_name = 'value_sum'
	
	# Initialize list of classes w/ the first class.
	color_classes = [get_color_class(attr=attr_name, cmax=value_min, hsv=colormap['ys'][0])]

	# Create the middle classes.
	for n in range(1, num_classes):

		# Set scaled bounds.
		scaled_xmin = float(n)/num_classes
		scaled_xmax = float(n+1)/num_classes

		# Set the value bounds for the class.
		cmin = value_min + scaled_xmin * value_range
		cmax = value_min + scaled_xmax * value_range
		
		# Get the index of the closest colormap entry <= the scaled position.
		cm_i = bisect.bisect_left(colormap['xs'], scaled_xmin)

		# If at the edge of the colormap, then use the last color.
		if cm_i == len(colormap['xs']) - 1: ccolor = colormap['ys'][cm_i]

		# Otherwise interpolate the color.
		else: ccolor = interpolate_ntuple(colormap['xs'][cm_i], colormap['xs'][cm_i + 1], colormap['ys'][cm_i], colormap['ys'][cm_i + 1], scaled_xmin, 3)
		
		# Create the color class.
		color_classes.append(get_color_class(attr=attr_name, cmin=cmin, cmax=cmax, hsv=ccolor))
	
	# Create the last color class.
	color_classes.append(get_color_class(attr=attr_name, cmin=value_max, hsv=colormap['ys'][-1]))

	# Process mapfile template.
	mapfile_template = env.get_template('results.mapfile.tpl')
	mapfile_content = mapfile_template.render(
		img_width = 800,
		img_height = 800,
		base_layers = base_layers,
		field_data_source = field_data_source,
		color_classes = color_classes
	)

	# Write processed template to a tmp mapfile.
	tmp_file_path = "/tmp/%s.map" % os.getpid()
	tmp_file = open(tmp_file_path, 'wb')
	tmp_file.write(mapfile_content)
	tmp_file.close()

	# Create map image from template.
	ms_map = mapscript.mapObj(tmp_file_path)
	map_img = ms_map.draw()

	# Remove tmp mapfile.
	os.remove(tmp_file_path)

	# Crop map image via PIL.
	im = Image.open(StringIO(map_img.getBytes()))
	(w,h) = im.size
	cropped_im = im.crop(tuple([int(d) for d in [w * .33, 0, w * .70, h*.88]]))

	# Return image.
	cropped_im.show()

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

def get_default_colormap():
	start_hsv = (0.0,0.0,0.0)
	end_hsv = (0.0,0.0,255.0)
	colormap = {'xs': [0], 'ys': [start_hsv]}
	num_classes = 10
	for n in range(1, num_classes):
		x = 1.0 * n/num_classes
		y = interpolate_ntuple(0.0, 1.0, start_hsv, end_hsv, x, 3)
		colormap['xs'].append(x)
		colormap['ys'].append(y)
	return colormap

def interpolate(start_x, end_x, start_y, end_y, x):
	x_range = end_x - start_x
	y_range = end_y - start_y
	return start_y + (x - start_x)/x_range * y_range

def interpolate_ntuple(start_x, end_x, start_y, end_y, x, n):
	return tuple([interpolate(start_x, end_x, start_y[i], end_y[i], x)  for i in range(n)])

if __name__ == '__main__': main()
