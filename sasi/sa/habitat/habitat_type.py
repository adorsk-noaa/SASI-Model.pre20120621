from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint, Integer, String, Float
from sqlalchemy.orm import relationship, mapper
from geoalchemy import *
from geoalchemy.postgis import PGComparator

from sasi.habitat.habitat_type import Habitat_Type
from sasi.habitat.substrate import Substrate
import sasi.sa.habitat.substrate as sa_substrate

import sasi.sa.metadata as sa_metadata
metadata = sa_metadata.metadata

table = Table('habitat_type', metadata,
		Column('id', String, primary_key=True),
		Column('substrate_id', String),
		Column('energy', String),
		ForeignKeyConstraint(['substrate_id'], [sa_substrate.table.c.id], deferrable=True),
		)

GeometryDDL(table)

mapper(
		Habitat_Type,
		table,
		properties = {
		'substrate': relationship(Substrate, lazy='joined'),
		})

