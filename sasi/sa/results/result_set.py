from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, mapper

import sasi.sa.metadata as sa_metadata

from sasi.results.result import Result
from sasi.results.result_set import Result_Set

import sasi.sa.results.result as sa_result

metadata = sa_metadata.metadata

result_set_table = Table('result_set', metadata,
		Column('id', String, primary_key=True),
		)

result_set_result_table = Table('result_set_result', metadata,
		Column('result_set_id', String, ForeignKey(result_set_table.c.id), primary_key=True),
		Column('result_id', Integer, ForeignKey(sa_result.table.c.id), primary_key=True)
		)

mapper(
		Result_Set, 
		result_set_table,
		properties = {
			'results': relationship(Result, cascade='all', secondary=result_set_result_table)
			}
	)