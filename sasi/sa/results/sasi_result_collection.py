from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, mapper

import sasi.sa.metadata as sa_metadata

from sasi.results.sasi_result import SASI_Result
from sasi.results.sasi_result_collection import SASI_Result_Collection

metadata = sa_metadata.metadata

table = Table('sasi_result_collection', metadata,
		Column('id', String, primary_key=True),
		)

mapper(
		SASI_Result_Collection, 
		table,
		properties = {
			'results': relationship(SASI_Result, cascade='all, delete, delete-orphan')
			}
	)
