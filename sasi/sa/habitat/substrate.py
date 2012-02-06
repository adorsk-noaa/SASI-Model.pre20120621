from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapper
from sasi.habitat.substrate import Substrate

metadata = MetaData()

table = Table('substrate', metadata,
		Column('id', String, primary_key=True),
		Column('name', String)
		)
		
mapper(Substrate, table)
