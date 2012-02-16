from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, mapper
from geoalchemy import *
from geoalchemy.postgis import PGComparator

from sasi.habitat.habitat_type import Habitat_Type
from sasi.habitat.habitat import Habitat
import sasi.sa.habitat.habitat_type as sa_habitat_type

import sasi.sa.metadata as sa_metadata
metadata = sa_metadata.metadata

table = Table('habitat', metadata,
		Column('id', Integer, primary_key=True),
		Column('id_km100', Integer),
		Column('id_km1000', Integer),
		Column('id_vor', Integer),
		Column('habitat_type_id', String, ForeignKey(sa_habitat_type.table.c.id)),
		Column('z', Float),
		Column('area', Float),
		GeometryExtensionColumn('geom', MultiPolygon(2)),
		)

GeometryDDL(table)

mapper(
		Habitat,
		table,
		properties = {
		'geom': GeometryColumn(table.c.geom, comparator=PGComparator),
		'habitat_type': relationship(Habitat_Type, cascade='merge'),
		})

