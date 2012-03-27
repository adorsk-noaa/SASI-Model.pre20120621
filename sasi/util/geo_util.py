from shapely import wkb, wkt
import types

def generate_multipolygon(wkb=False):
	wkt_poly = 'MULTIPOLYGON(((0 0, 1 0, 1 1, 0 1, 0 0)))'
	if wkb: 
		geom = wkt.loads(wkt_poly)
		geom.geom_wkb = geom.wkb
	else: geom = wkt_poly
	return geom


