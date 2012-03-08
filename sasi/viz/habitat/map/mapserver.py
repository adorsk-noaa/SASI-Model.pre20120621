"""
Mapserver implementations of mapping methods for habitat maps.
"""
import mapscript
import sys, os

# Get a habitat map from a WMS parameters and custom parameters.
def get_map_image_from_wms(parameters=None, habitat_dao=None):

	# Initialize mapscript map object from the habitat mapfile template.
	mapfile = "%s/habitat.map" % os.path.abspath(os.path.dirname(__file__))
	ms_map = mapscript.mapObj(mapfile)

	"""
	# Build WMS request from parameters.
	wms_request = mapscript.OWSRequest()
	for k, v in parameters.get('wms', {}).items():
		wms_request.setParameter(k,v)
	
	# Load the parameters into the map.
	ms_map.loadOWSParameters(wms_request)
	"""

	# Set the habitat layer's connection parameters.
	connection_str = ""
	
	# Build data string based on custom parameters.
	data_str = ""
	
	# Draw the map.
	ms_image = ms_map.draw()

	# Return the raw image.
	return ms_image.getBytes()
	"""


