import sasi.sa.session as sa_session
import sasi.sa.metadata as sa_metadata
import sasi.sa.fishing.gear as sa_gear

def create_schema():
	
	session = sa_session.get_session()
	sa_gear.table.create(session.bind)


