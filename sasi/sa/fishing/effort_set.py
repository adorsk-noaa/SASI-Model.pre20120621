from sqlalchemy import Table, Column, ForeignKey, ForeignKeyConstraint, Integer, String, Float
from sqlalchemy.orm import relationship, mapper

import sasi.sa.metadata as sa_metadata

from sasi.fishing.effort import Effort
from sasi.fishing.effort_set import Effort_Set

import sasi.sa.fishing.effort as sa_effort

metadata = sa_metadata.metadata

effort_set_table = Table('effort_set', metadata,
		Column('id', String, primary_key=True),
		)

effort_set_effort_table = Table('effort_set_effort_', metadata,
		Column('effort_set_id', String, primary_key=True),
		Column('effort_id', Integer, primary_key=True),
		ForeignKeyConstraint(['effort_set_id'],[effort_set_table.c.id], deferrable=True),
		ForeignKeyConstraint(['effort_id'],[sa_effort.table.c.id], deferrable=True),
		)

mapper(
		Effort_Set, 
		effort_set_table,
		properties = {
			'efforts': relationship(Effort, cascade='all', secondary=effort_set_effort_table)
			}
	)
