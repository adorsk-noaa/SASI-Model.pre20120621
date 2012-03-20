"""
Mapserver implementations of mapping methods for habitat maps.
"""
import mapscript
import sys, os

# Get a habitat map from a WMS parameters and custom parameters.
# @TODO: empirically, nx=12 and maxfeatures=1000 gets reasonable results.
def get_map_image_from_wms(wms_parameters=None, habitat_dao=None, filters=[]):

	# Initialize mapscript map object from the habitat mapfile template.
	mapfile = "%s/habitat.map" % os.path.abspath(os.path.dirname(__file__))
	ms_map = mapscript.mapObj(mapfile)


	# Generate tiled data layers.

	# Get bounds for each tile.
	nx = 12
	ny = nx
	minx = -79.0
	miny = 31.0
	maxx = -65.0
	maxy = 45.0
	dx = (maxx - minx)/nx
	dy = (maxy - miny)/ny
	
	xs = [minx + n * dx for n in range(nx+1)]
	ys = [miny + n * dy for n in range(ny+1)]

	xpairs = [(xs[i], xs[i+1]) for i in range(len(xs) - 1)]
	ypairs = [(ys[i], ys[i+1]) for i in range(len(ys) - 1)]

	tiles = []
	for xp in xpairs:
		for yp in ypairs:
			tiles.append([xp[0], yp[0], xp[1], yp[1]])
	
	# Define a layer for each tile.
	i = 0
	for t in tiles:
		layer = mapscript.layerObj()
		layer.name = "layer_%s" % i 
		layer.group = 'data'

		layer.type = mapscript.MS_LAYER_POLYGON

		layer.setConnectionType(mapscript.MS_POSTGIS, '')
		connection_str = habitat_dao.get_mapserver_connection_string()
		layer.connection = connection_str
		data_str = habitat_dao.get_mapserver_data_string(filters=filters)
		layer.data = data_str
		layer.setProcessingKey('CLOSE_CONNECTION', 'DEFER')

		layer.maxfeatures = 1000

		layer.setExtent(*t)

		layer.setProjection('init=epsg:4326')

		clz = mapscript.classObj()
		clz.name = 'clz'
		style = mapscript.styleObj()
		style.color= mapscript.colorObj((i * 10) % 255,1 + ((i*10) % 255)/2,1)
		clz.insertStyle(style)
		layer.insertClass(clz)

		layer.status = mapscript.MS_DEFAULT

		ms_map.insertLayer(layer)
		i += 1
	
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

"""
def get_map_image_from_wms(wms_parameters=None, habitat_dao=None, filters=None):

	# Initialize mapscript map object from the habitat mapfile template.
	mapfile = "%s/habitat.map" % os.path.abspath(os.path.dirname(__file__))
	ms_map = mapscript.mapObj(mapfile)

	# Build WMS request from parameters.
	wms_request = mapscript.OWSRequest()
	for k, v in wms_parameters:
		wms_request.setParameter(k,v)

	# Load the parameters into the map.
	ms_map.loadOWSParameters(wms_request)

	# Get the habitat layer.
	layer = ms_map.getLayerByName('habitat')

	# Set connection type to be POSTGIS.
	layer.setConnectionType(mapscript.MS_POSTGIS, '')

	# Set the habitat layer's connection parameters.
	connection_str = habitat_dao.get_mapserver_connection_string()
	layer.connection = connection_str
	
	# Build data string based on custom parameters.
	data_str = habitat_dao.get_mapserver_data_string(filters=filters)
	layer.data = data_str
	
	# Draw the map.
	ms_image = ms_map.draw()

	# Return the raw image.
	return ms_image.getBytes()
"""

