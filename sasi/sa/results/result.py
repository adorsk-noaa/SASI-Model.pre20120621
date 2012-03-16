from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint, Integer, String, Float
from sqlalchemy.orm import relationship, mapper

import sasi.sa.metadata as sa_metadata

from sasi.results.result import Result
from sasi.habitat.cell import Cell
from sasi.habitat.habitat_type import Habitat_Type
from sasi.habitat.feature import Feature
from sasi.fishing.gear import Gear

import sasi.sa.habitat.cell as sa_cell
import sasi.sa.habitat.habitat_type as sa_habitat_type
import sasi.sa.habitat.feature as sa_feature
import sasi.sa.fishing.gear as sa_gear

metadata = sa_metadata.metadata

table = Table('result', metadata,
		Column('id', Integer, primary_key=True),
		Column('time', Integer),
		Column('cell_id', Integer),
		Column('habitat_type_id', String),
		Column('gear_id', String),
		Column('feature_id', String),
		Column('tag', String),
		Column('field', String),
		Column('value', Float),
		ForeignKeyConstraint(['cell_id'], [sa_cell.cell_table.c.id], deferrable=True),
		ForeignKeyConstraint(['habitat_type_id'], [sa_habitat_type.habitat_type_table.c.id], deferrable=True),
		ForeignKeyConstraint(['gear_id'], [sa_gear.table.c.id], deferrable=True),
		ForeignKeyConstraint(['feature_id'], [sa_feature.table.c.id], deferrable=True),
		)

mapper(
		Result, 
		table,
		properties = {
			'cell': relationship(Cell),
			'habitat_type': relationship(Habitat_Type),
			'gear': relationship(Gear),
			'feature': relationship(Feature),
			}
	)



