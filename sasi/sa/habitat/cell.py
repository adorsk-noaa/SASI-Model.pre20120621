from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapper
from geoalchemy import *
from geoalchemy.postgis import PGComparator
from sasi.habitat.cell import Cell

metadata = MetaData()

cell_table = Table('cell', metadata,
		Column('id_100km', Integer, primary_key=True),
		Column('id_1000km', Integer),
		GeometryExtensionColumn('geom', MultiPolygon(2))
		)
		
GeometryDDL(cell_table)

mapper(Cell, cell_table, properties = {
	'geom': GeometryColumn(cell_table.c.geom, comparator=PGComparator)
	})
			
