from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint, Integer, String, Float
from sqlalchemy.orm import relationship, mapper

import sasi.sa.metadata as sa_metadata

from sasi.fishing.effort import Effort
from sasi.habitat.cell import Cell
from sasi.fishing.gear import Gear

import sasi.sa.habitat.cell as sa_cell
import sasi.sa.fishing.gear as sa_gear

metadata = sa_metadata.metadata

table = Table('effort', metadata,
		Column('cell_id', Integer, primary_key=True),
		Column('time', Integer,primary_key=True),
		Column('gear_id', String,primary_key=True),
		Column('tag', String,primary_key=True),
		Column('swept_area', Float),
		Column('hours_fished', Float),
		ForeignKeyConstraint(['cell_id'], [sa_cell.cell_table.c.id], deferrable=True),
		ForeignKeyConstraint(['gear_id'],[sa_gear.table.c.id], deferrable=True),
		)

mapper(
		Effort, 
		table,
		properties = {
			'cell': relationship(Cell, lazy='joined'),
			'gear': relationship(Gear, lazy='joined'),
			}
	)



