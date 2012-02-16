from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapper
from sasi.fishing.gear import Gear

import sasi.sa.metadata as sa_metadata
metadata = sa_metadata.metadata

table = Table('gear', metadata,
		Column('id', String, primary_key=True),
		Column('name', String),
		)
		
mapper(Gear, table)
