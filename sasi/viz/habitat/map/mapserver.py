"""
Mapserver implementations of mapping methods for habitat maps.
"""
import mapscript
import sys, os

# Get a habitat map from a WMS parameters and custom parameters.
def get_map_image_from_wms(wms_parameters=None, habitat_dao=None, filters=None):

	# Initialize mapscript map object from the habitat mapfile template.
	mapfile = "%s/habitat.map" % os.path.abspath(os.path.dirname(__file__))
	ms_map = mapscript.mapObj(mapfile)

	# Build WMS request from parameters.
	wms_request = mapscript.OWSRequest()
	for k, v in wms_parameters.items():
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


