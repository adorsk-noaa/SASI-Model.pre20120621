"""
Mapserver implementations of mapping methods for habitat maps.
"""
import mapscript
import sys, os, re, struct

# Get a habitat map from a WMS parameters and custom parameters.
# @TODO: empirically, nx=12 and maxfeatures=1000 gets reasonable results.
def foo_get_map_image_from_wms(wms_parameters=None, habitat_dao=None, filters=[]):

	# Initialize mapscript map object from the habitat mapfile template.
	mapfile = "%s/habitat.map" % os.path.abspath(os.path.dirname(__file__))
	ms_map = mapscript.mapObj(mapfile)


	# Generate tiled data layers.

	# Get bounds for each tile.
	maxfeatures = 200
	nx = 50
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

	tiles = [[-69.25, 40.78, -69.12, 40.88]]
	

	# Get data string template.
	tile_stub = 'POLYGON((TILEPOLYGON))'
	tile_filter =  [{'field': 'geom', 'op': 'intersects', 'value': tile_stub}]
	data_str_template = habitat_dao.get_mapserver_data_string(filters= filters + tile_filter)

	# Define a layer for each tile.
	i = 0
	outline_layers = []

	#for t in tiles[63:65]:
	for t in tiles:
		layer = mapscript.layerObj()
		layer.name = "layer_%s" % i 
		layer.group = 'data'

		layer.debug = 2

		layer.type = mapscript.MS_LAYER_POLYGON
		layer.setExtent(*t)

		layer.setProjection('init=epsg:4326')

		layer.status = mapscript.MS_DEFAULT

		# Create inline feature layer for show tile bounds.
		outline_layer = layer.clone()
		outline_layer.name = "outline_layer_%s" % i 
		outline_clz = mapscript.classObj()
		outline_clz.name = 'clz'
		outline_style = mapscript.styleObj()
		outline_style.outlinecolor= mapscript.colorObj(0,0,0)
		outline_style.width = 3
		outline_clz.insertStyle(outline_style)
		outline_layer.insertClass(outline_clz)
		outline_feature = mapscript.shapeObj(mapscript.MS_SHAPE_POLYGON)
		tile_wkt = "POLYGON((%s %s, %s %s, %s %s, %s %s, %s %s))" % (t[0], t[1], t[0], t[3], t[2], t[3], t[2], t[1], t[0], t[1])
		outline_feature = outline_feature.fromWKT(tile_wkt)
		outline_layer.addFeature(outline_feature)
		outline_layers.append(outline_layer)


		layer.setConnectionType(mapscript.MS_POSTGIS, '')
		connection_str = habitat_dao.get_mapserver_connection_string()
		layer.connection = connection_str

		# Replace geo filter in data string with tile bounds.
		data_str = re.sub(re.escape(tile_stub), tile_wkt, data_str_template)
		layer.data = data_str
		layer.setProcessingKey('CLOSE_CONNECTION', 'DEFER')

		line_layer = layer.clone()
		line_clz = mapscript.classObj()
		line_clz.name = 'clz'
		line_style = mapscript.styleObj()
		line_style.outlinecolor= mapscript.colorObj(0,0,0)
		line_style.width = .5 
		line_clz.insertStyle(line_style)
		line_layer.insertClass(line_clz)
		ms_map.insertLayer(line_layer)

	
		layer.maxfeatures = maxfeatures



		clz = mapscript.classObj()
		clz.name = 'clz'
		style = mapscript.styleObj()
		#style.color= mapscript.colorObj((i) % 255, 1,1)
		style.color= mapscript.colorObj(128, 1,1)
		style.outlinecolor= mapscript.colorObj(0,0,0)
		style.width = .5 
		clz.insertStyle(style)
		layer.insertClass(clz)


		ms_map.insertLayer(layer)

		i += 1
	
	"""
	for ol in outline_layers:
		ms_map.insertLayer(ol)
	"""
	
	pid = os.getpid()
	ms_map.setConfigOption('MS_ERRORFILE', '/tmp/map_log.%s.txt' % pid)
	
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

def get_map_image_from_wms(wms_parameters=None, habitat_dao=None, filters=None):

	# Initialize mapscript map object from the habitat mapfile template.
	mapfile = "%s/habitat.map" % os.path.abspath(os.path.dirname(__file__))
	ms_map = mapscript.mapObj(mapfile)

	layer = mapscript.layerObj()
	layer.name = "data" 
	layer.group = 'data'

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
