# Populates cell table.
# Assumes that habitats have already been loaded into db.
from sasi.habitat.habitat import Habitat
from sasi.habitat.cell import Cell

import sasi.sa.session as sa_session
import sasi.sa.habitat.habitat as sa_habitat
import sasi.sa.habitat.cell as sa_cell

from sqlalchemy.sql import func
from geoalchemy.functions import functions as geo_func

from shapely import wkb
from shapely.geometry import Polygon, MultiPolygon

def main():

	# Get db session.
	session = sa_session.get_session()

	# Drop/Create Cell Tables.	
	sa_cell.metadata.drop_all(session.bind)
	sa_cell.metadata.create_all(session.bind)
	session.commit()

	# For each type of cell...
	for cell_size in ['km100', 'km1000']:

		print "Processing cells of size '%s'" % cell_size

		# Initialize list of cells.
		cells = []

		# Get cell ids
		cell_id_attr = getattr(Habitat, "id_%s" % cell_size)
		cell_area = func.sum(geo_func.area(Habitat.geom)).label('cell_area')
		cell_geom_wkb = geo_func.wkb(func.st_union(Habitat.geom).label('cell_geom'))
		cell_infos = session.query(cell_id_attr, cell_area, cell_geom_wkb).group_by(cell_id_attr).all()

		# For each id, create cell and assign habitats.
		print "Creating cells"

		cell_counter = 0
		for (cell_id, cell_area, cell_geom_wkb) in cell_infos:

			if (cell_counter % 1000) == 0: print "%s..." % (cell_counter),
			cell_counter += 1	

			# Get cell's habitats.
			cell_habitats = session.query(Habitat).filter(cell_id_attr == cell_id).all()

			# Format cell's geometry.
			cell_geom = wkb.loads("%s" % cell_geom_wkb)
			if cell_geom.geom_type =='Polygon':
				cell_geom = MultiPolygon([(cell_geom.exterior.coords, cell_geom.interiors )])

			cell = Cell(
					type = cell_size,
					type_id = cell_id,
					geom = cell_geom.wkt,
					area = cell_area,
					habitats = cell_habitats
					)

			cells.append(cell)
		
		session.add_all(cells)	
		session.commit()
			

if __name__ == '__main__':
	main()
