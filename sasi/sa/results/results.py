import sasi.sa.session as sa_session
import sasi.sa.metadata as sa_metadata
import sasi.sa.results.result as sa_result

def create_schema():
	
	session = sa_session.get_session()

	tables = [
			sa_result.table
			]

	for t in tables: 
		if t.exists(session.bind): t.drop(session.bind)
	tables.reverse()	
	for t in tables: t.create(session.bind)	



