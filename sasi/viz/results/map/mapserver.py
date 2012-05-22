"""
Functions for creating result maps via MapServer.
"""

import mapscript
import sys, os, re, struct
import colorsys
import bisect


def get_map_image_from_wms(wms_parameters=None, result_field=None, result_dao=None, filters=[], color_map={}):

	# Initialize mapscript map object from the habitat mapfile template.
	mapfile = "%s/results.map" % os.path.abspath(os.path.dirname(__file__))
	ms_map = mapscript.mapObj(mapfile)

	layer = mapscript.layerObj()
	layer.name = "data" 

	layer.setProjection('init=epsg:4326')
	layer.status = mapscript.MS_DEFAULT
	layer.setConnectionType(mapscript.MS_POSTGIS, '')
	connection_str = result_dao.get_mapserver_connection_string()
	layer.connection = connection_str
	layer.data = result_dao.get_mapserver_data_string(result_field=result_field, filters=filters)

	layer.type = mapscript.MS_LAYER_POLYGON

	# Get color range settings.
	num_classes = result_field.get('num_classes', 10)

	if not color_map: color_map = get_default_colormap()

	# Get color classes.
	color_classes = get_color_classes(
			attr='value_field', 
			vmin = result_field.get('min', 0),
			vmax = result_field.get('max', 1),
			num_classes= result_field.get('num_classes', 10), 
			color_map=color_map
			)

	# Create classes for value ranges.
	"""
	clz = mapscript.classObj()
	clz.name = 'data'
	style = mapscript.styleObj()
	rgb_color = (255,0,0)
	style.color= mapscript.colorObj(*rgb_color)
	clz.insertStyle(style)
	layer.insertClass(clz)
	"""
	for cc in color_classes:
		layer.insertClass(cc)

	ms_map.insertLayer(layer)

	# Build WMS request from parameters.
	wms_request = mapscript.OWSRequest()
	for k, v in wms_parameters:
		wms_request.setParameter(k,v)

	# Load the parameters into the map.
	ms_map.loadOWSParameters(wms_request)

	# Draw the map.
	ms_image = ms_map.draw()

	# Return the raw image.
	return ms_image.getBytes()


def get_color_classes(attr='', vmin=0, vmax=1, num_classes=10, color_map={}):

	vrange = vmax - vmin

	# Initialize list of classes w/ the first class.
	color_classes = [get_color_class(attr=attr, cmax=vmin, hsv=color_map['ys'][0])]

	# Create the middle classes.
	for n in range(1, num_classes):

		# Set scaled bounds.
		scaled_xmin = float(n)/num_classes
		scaled_xmax = float(n+1)/num_classes

		# Set the value bounds for the class.
		cmin = vmin + scaled_xmin * vrange
		cmax = vmin + scaled_xmax * vrange
		
		# Get the index of the closest colormap entry <= the scaled position.
		cm_i = bisect.bisect_left(color_map['xs'], scaled_xmin)

		# If at the edge of the colormap, then use the last color.
		if cm_i == len(color_map['xs']) - 1: ccolor = color_map['ys'][cm_i]

		# Otherwise interpolate the color.
		else: ccolor = interpolate_ntuple(color_map['xs'][cm_i], color_map['xs'][cm_i + 1], color_map['ys'][cm_i], color_map['ys'][cm_i + 1], scaled_xmin, 3)
		
		# Create the color class.
		color_classes.append(get_color_class(attr=attr, cmin=cmin, cmax=cmax, hsv=ccolor))
	
	# Create the last color class.
	color_classes.append(get_color_class(attr=attr, cmin=vmax, hsv=color_map['ys'][-1]))

	return color_classes


def get_color_class(attr=None, cmin=None, cmax=None, hsv=None):

	clz = mapscript.classObj()
	clz.name = "{} to {}".format(cmin, cmax)
	style = mapscript.styleObj()
	rgb = [int(c) for c in colorsys.hsv_to_rgb(*hsv)]
	style.color= mapscript.colorObj(*rgb)
	clz.insertStyle(style)

	criteria = []
	if cmin != None: criteria.append("[{}] >= {}".format(attr, cmin))
	if cmax != None: criteria.append("[{}] < {}".format(attr, cmax))

	if criteria:
		expression = "({})".format(' AND '.join(criteria))
		clz.setExpression(expression)

	return clz


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
