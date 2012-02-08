from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, mapper
from geoalchemy import *
from geoalchemy.postgis import PGComparator

from sasi.habitat.cell import Cell
from sasi.habitat.habitat import Habitat

import sasi.sa.habitat.habitat as sa_habitat

metadata = MetaData()

cell_table = Table('cell', metadata,
		Column('id', Integer, primary_key=True),
		Column('type', String),
		Column('type_id', String),
		Column('area', Float),
		GeometryExtensionColumn('geom', MultiPolygon(2)),
		)

GeometryDDL(cell_table)

cell_habitat_table = Table('cell_habitat', metadata,
		Column('cell_id', Integer, ForeignKey(cell_table.c.id), primary_key=True),
		Column('habitat_id', Integer, ForeignKey(sa_habitat.habitat_table.c.id), primary_key=True),
		)

mapper(
		Cell, 
		cell_table,
		properties = {
			'geom': GeometryColumn(cell_table.c.geom, comparator=PGComparator),
			'habitats': relationship(Habitat, cascade='merge', secondary=cell_habitat_table)
			}
	)



