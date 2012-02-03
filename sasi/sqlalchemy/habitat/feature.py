from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapper
from sasi.habitat.feature import Feature

metadata = MetaData()

table = Table('feature', metadata,
		Column('id', String, primary_key=True),
		Column('name', String),
		Column('category', String)
		)
		
mapper(Feature, table)
