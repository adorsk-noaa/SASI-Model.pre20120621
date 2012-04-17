"""
Mapserver implementations of mapping methods for habitat maps.
"""
import mapscript
import sys, os, re, struct

def get_map_image_from_wms(wms_parameters=None, habitat_dao=None, filters=None):

	# Initialize mapscript map object from the habitat mapfile template.
	mapfile = "%s/habitat.map" % os.path.abspath(os.path.dirname(__file__))
	ms_map = mapscript.mapObj(mapfile)

	layer = mapscript.layerObj()
	layer.name = "habitat" 

	layer.setProjection('init=epsg:4326')
	layer.status = mapscript.MS_DEFAULT
	layer.setConnectionType(mapscript.MS_POSTGIS, '')
	connection_str = habitat_dao.get_mapserver_connection_string()
	layer.connection = connection_str
	layer.data = habitat_dao.get_mapserver_data_string(filters=filters)

	layer.type = mapscript.MS_LAYER_POLYGON

	# Create classes for types of substrates.

	substrate_styles= [
			{'name': 'S1', 'color': '8DD3C7'},
			{'name': 'S2', 'color': 'FFFFB3'},
			{'name': 'S3', 'color': 'BEBADA'},
			{'name': 'S4', 'color': 'FB8072'},
			{'name': 'S5', 'color': '80B1D3'},
			]

	for ss in substrate_styles:
		clz = mapscript.classObj()
		clz.name = ss['name']
		expression = "('[substrate_id]' eq '%s')" % ss['name']
		clz.setExpression(expression)
		style = mapscript.styleObj()
		rgb_color = hex_to_rgb(ss['color'])
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

def hex_to_rgb(hexstr): 
	return struct.unpack('BBB',hexstr.decode('hex'))

def rgb_to_hex(rgb): 
	struct.pack('BBB',*rgb).encode('hex')
