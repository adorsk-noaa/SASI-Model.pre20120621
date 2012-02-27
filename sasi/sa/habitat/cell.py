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
		Column('type', String, primary_key=True),
		Column('type_id', String, primary_key=True),
		Column('area', Float),
		Column('depth', Float),
		GeometryExtensionColumn('geom', MultiPolygon(2)),
		)

GeometryDDL(cell_table)

cell_habitat_table = Table('cell_habitat', metadata,
		Column('cell_type', String, primary_key=True),
		Column('cell_type_id', String, primary_key=True),
		Column('habitat_id', Integer, primary_key=True),
		ForeignKeyConstraint(['cell_type', 'cell_type_id'], [cell_table.c.type, cell_table.c.type_id], deferrable=True),
		ForeignKeyConstraint(['habitat_id'], [sa_habitat.table.c.id], deferrable=True),
		)

mapper(
		Cell, 
		cell_table,
		properties = {
			'geom': GeometryColumn(cell_table.c.geom, comparator=PGComparator),
			'habitats': relationship(Habitat, secondary=cell_habitat_table, lazy='subquery')
			}
	)



