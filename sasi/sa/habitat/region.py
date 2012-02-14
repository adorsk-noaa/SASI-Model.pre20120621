from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, mapper
from geoalchemy import *
from geoalchemy.postgis import PGComparator

from sasi.habitat.habitat import Habitat
from sasi.habitat.region import Region
import sasi.sa.habitat.habitat as sa_habitat

import sasi.sa.metadata as sa_metadata
metadata = sa_metadata.metadata

table = Table('region', metadata,
		Column('id', Integer, primary_key=True),
		Column('habitat_id', String, ForeignKey(sa_habitat.table.c.id)),
		Column('z', Float),
		Column('area', Float),
		GeometryExtensionColumn('geom', MultiPolygon(2)),
		)

GeometryDDL(table)

mapper(
		Region,
		table,
		properties = {
		'geom': GeometryColumn(table.c.geom, comparator=PGComparator),
		'habitat': relationship(Habitat, cascade='all'),
		})

