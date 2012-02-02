# Populates table of grid cell info from shapefile.

import sasi.conf
from sasi.habitat.cell import Cell
import sasi.sqlalchemy.session as sa_session
import sasi.sqlalchemy.habitat.cell as sa_cell
import ogr
from shapely import wkb
from shapely.geometry import Polygon, MultiPolygon

def main():

	# Load shapefile
	sf = ogr.Open(sasi.conf.conf['grid_file'])
	
	# Get cell feature layer.
	layer = sf.GetLayer(0)

	# Get fields.
	layer_def = layer.GetLayerDefn()
	field_count = layer_def.GetFieldCount()
	fields = [layer_def.GetFieldDefn(i).GetName() for i in range(field_count)]

	# Initialize a list to hold cell objects.
	cells = []

	print fields
	# For each cell feature... 
	for f in layer:
		# Get feature geometry. We convert each feature into a multipolygon, since
		# we may have a mix of normal polygons and multipolygons.
		geom = wkb.loads(f.GetGeometryRef().ExportToWkb())
		if geom.geom_type =='Polygon':
			geom = MultiPolygon([(geom.exterior.coords, geom.interiors )])

		# Get feature attributes.
		f_attributes = {}
		for i in range(field_count): 
			f_attributes[fields[i]] = f.GetField(i)

		# Make cell object from feature data.
		c = Cell(
				id_100km = f_attributes['100km_Id'],
				id_1000km = f_attributes['1000Km_Id'],
				geom = geom.wkt
				)
		cells.append(c)

	# Clear db of cells.
	session = sa_session.get_session()
	#session.execute(sa_cell.cell_table.delete())
	#session.commit()
	sa_cell.metadata.drop_all(session.bind)
	sa_cell.metadata.create_all(session.bind)

	# Save new cells.
	#session.add_all(cells)
	for c in cells:
		try:
			session.add(c)
			session.commit()
		except Exception as e:
			print e
			print "bad cell"
			print c.id_100km
			exit()


if __name__ == '__main__':
	main()
