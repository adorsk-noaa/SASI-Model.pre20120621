from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, mapper
from geoalchemy import *
from geoalchemy.postgis import PGComparator

from sasi.habitat.cell import Cell
from sasi.habitat.region import Region

import sasi.sa.habitat.region as sa_region

import sasi.sa.metadata as sa_metadata
metadata = sa_metadata.metadata

cell_table = Table('cell', metadata,
		Column('id', Integer, primary_key=True),
		Column('type', String),
		Column('type_id', String),
		Column('area', Float),
		GeometryExtensionColumn('geom', MultiPolygon(2)),
		)

GeometryDDL(cell_table)

cell_region_table = Table('cell_region', metadata,
		Column('cell_id', Integer, ForeignKey(cell_table.c.id), primary_key=True),
		Column('region_id', Integer, ForeignKey(sa_region.table.c.id), primary_key=True),
		)

mapper(
		Cell, 
		cell_table,
		properties = {
			'geom': GeometryColumn(cell_table.c.geom, comparator=PGComparator),
			'regions': relationship(Region, cascade='all', secondary=cell_region_table)
			}
	)



