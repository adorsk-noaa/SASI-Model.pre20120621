import sasi.sa.session as sa_session
import sasi.sa.metadata as sa_metadata
import sasi.sa.results.sasi_result as sa_sasi_result
import sasi.sa.results.sasi_result_collection as sa_sasi_result_collection

def create_schema():
	
	session = sa_session.get_session()
	sa_sasi_result_collection.table.create(session.bind)
	sa_sasi_result.table.create(session.bind)


