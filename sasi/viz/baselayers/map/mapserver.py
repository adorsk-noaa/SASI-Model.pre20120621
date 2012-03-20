"""
Mapserver implementations of mapping methods for baselayer maps.
"""
import mapscript
import sys, os

# Get a habitat map from a WMS parameters and custom parameters.
def get_map_image_from_wms(wms_parameters=None):

	# Initialize mapscript map object from the baselayers mapfile template.
	mapfile = "%s/baselayers.map" % os.path.abspath(os.path.dirname(__file__))
	ms_map = mapscript.mapObj(mapfile)

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

