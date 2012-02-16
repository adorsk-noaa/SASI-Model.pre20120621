from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, mapper

import sasi.sa.metadata as sa_metadata

from sasi.results.sasi_result import SASI_Result
from sasi.habitat.cell import Cell
from sasi.habitat.habitat_type import Habitat_Type
from sasi.habitat.feature import Feature
from sasi.fishing.gear import Gear

import sasi.sa.habitat.cell as sa_cell
import sasi.sa.habitat.habitat_type as sa_habitat_type
import sasi.sa.habitat.feature as sa_feature
import sasi.sa.fishing.gear as sa_gear


metadata = sa_metadata.metadata

table = Table('sasi_result', metadata,
		Column('id', Integer, primary_key=True),
		Column('time', String),
		Column('cell_id', Integer, ForeignKey(sa_cell.cell_table.c.id)),
		Column('habitat_type_id', String, ForeignKey(sa_habitat_type.table.c.id)),
		Column('gear_id', String, ForeignKey(sa_gear.table.c.id)),
		Column('feature_id', String, ForeignKey(sa_feature.table.c.id)),
		Column('field', String),
		Column('value', String),
		)

mapper(
		SASI_Result, 
		table,
		properties = {
			'cell': relationship(Cell, cascade='merge'),
			'habitat_type': relationship(Habitat_Type, cascade='merge'),
			'gear': relationship(Gear, cascade='merge'),
			'feature': relationship(Feature, cascade='merge'),
			}
	)



