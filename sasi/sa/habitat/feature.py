from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapper
from sasi.habitat.feature import Feature

import sasi.sa.metadata as sa_metadata
metadata = sa_metadata.metadata

table = Table('feature', metadata,
		Column('id', String, primary_key=True),
		Column('name', String),
		Column('category', String)
		)
		
mapper(Feature, table)
