from shapely import wkb, wkt

def generate_multipolygon():
	return wkt.loads('MULTIPOLYGON(((0 0, 1 0, 1 1, 0 1, 0 0)))').wkb
