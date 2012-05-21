"""
Functions for creating result maps via MapServer.
"""

import mapscript
import sys, os, re, struct


def get_map_image_from_wms(wms_parameters=None, result_field=None, result_dao=None, filters=[]):

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

	# Create classes for value ranges.
	clz = mapscript.classObj()
	clz.name = 'data'
	style = mapscript.styleObj()
	rgb_color = (255,0,0)
	style.color= mapscript.colorObj(*rgb_color)
	clz.insertStyle(style)
	layer.insertClass(clz)

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

