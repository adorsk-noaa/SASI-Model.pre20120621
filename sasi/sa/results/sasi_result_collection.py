from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, mapper

import sasi.sa.metadata as sa_metadata

from sasi.results.sasi_result import SASI_Result
from sasi.results.sasi_result_collection import SASI_Result_Collection

import sasi.sa.results.sasi_result as sa_sasi_result

metadata = sa_metadata.metadata

sasi_result_collection_table = Table('sasi_result_collection', metadata,
		Column('id', Integer, primary_key=True),
		)

sasi_result_collection_sasi_result_table = Table('sasi_result_collection_sasi_result', metadata,
		Column('sasi_result_collection_id', Integer, ForeignKey(sasi_result_collection_table.c.id), primary_key=True),
		Column('sasi_result_id', Integer, ForeignKey(sa_sasi_result.table.c.id), primary_key=True),
		)

mapper(
		SASI_Result_Collection, 
		sasi_result_collection_table,
		properties = {
			'results': relationship(SASI_Result, cascade='merge', secondary=sasi_result_collection_sasi_result_table)
			}
	)
