from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, mapper
from geoalchemy import *
from geoalchemy.postgis import PGComparator

from sasi.habitat.habitat import Habitat
from sasi.habitat.substrate import Substrate
import sasi.sa.habitat.substrate as sa_substrate

import sasi.sa.metadata as sa_metadata
metadata = sa_metadata.metadata

table = Table('habitat', metadata,
		Column('id', String, primary_key=True),
		Column('substrate_id', String, ForeignKey(sa_substrate.table.c.id)),
		Column('energy', String),
		)

GeometryDDL(table)

mapper(
		Habitat,
		table,
		properties = {
		'substrate': relationship(Substrate, cascade='all'),
		})

