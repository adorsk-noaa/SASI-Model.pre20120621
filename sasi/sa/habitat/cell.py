from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint, Integer, String, Float
from sqlalchemy.orm import relationship, mapper
from geoalchemy import *
from geoalchemy.postgis import PGComparator

from sasi.habitat.cell import Cell
from sasi.habitat.habitat import Habitat

import sasi.sa.habitat.habitat as sa_habitat

import sasi.sa.metadata as sa_metadata
metadata = sa_metadata.metadata

cell_table = Table('cell', metadata,
		Column('id', Integer, primary_key=True),
		Column('type', String),
		Column('type_id', Integer),
		Column('area', Float),
		Column('depth', Float),
		GeometryExtensionColumn('geom', MultiPolygon(2)),
		)

GeometryDDL(cell_table)

cell_habitat_table = Table('cell_habitat', metadata,
		Column('cell_id', Integer, primary_key=True),
		Column('habitat_id', Integer, primary_key=True),
		ForeignKeyConstraint(['cell_id'], [cell_table.c.id], deferrable=True),
		ForeignKeyConstraint(['habitat_id'], [sa_habitat.table.c.id], deferrable=True),
		)

mapper(
		Cell, 
		cell_table,
		properties = {
			'geom': GeometryColumn(cell_table.c.geom, comparator=PGComparator),
			'habitats': relationship(Habitat, secondary=cell_habitat_table)
			}
	)



