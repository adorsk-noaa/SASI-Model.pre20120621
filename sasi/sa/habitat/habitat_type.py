from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint, Integer, String, Float
from sqlalchemy.orm import relationship, mapper
from geoalchemy import *
from geoalchemy.postgis import PGComparator

from sasi.habitat.habitat_type import Habitat_Type
from sasi.habitat.substrate import Substrate
from sasi.habitat.feature import Feature
import sasi.sa.habitat.substrate as sa_substrate
import sasi.sa.habitat.feature as sa_feature

import sasi.sa.metadata as sa_metadata
metadata = sa_metadata.metadata

habitat_type_table = Table('habitat_type', metadata,
		Column('id', String, primary_key=True),
		Column('substrate_id', String),
		Column('energy', String),
		ForeignKeyConstraint(['substrate_id'], [sa_substrate.table.c.id], deferrable=True),
		)

habitat_type_feature_table = Table('habitat_type_feature', metadata,
		Column('habitat_type_id', String, primary_key=True),
		Column('feature_id', String, primary_key=True),
		ForeignKeyConstraint(['habitat_type_id'], [habitat_type_table.c.id], deferrable=True),
		ForeignKeyConstraint(['feature_id'], [sa_feature.table.c.id], deferrable=True),
		)

mapper(
		Habitat_Type,
		habitat_type_table,
		properties = {
		'substrate': relationship(Substrate),
		'features': relationship(Feature, secondary=habitat_type_feature_table)
		})

