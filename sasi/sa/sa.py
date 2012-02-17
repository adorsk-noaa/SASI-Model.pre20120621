import sasi.sa.session as sa_session
import sasi.sa.metadata as sa_metadata
import sasi.sa.all_metadata as sa_all_metadata

def create_schema():

	s = sa_session.get_session()
	sa_metadata.metadata.drop_all(s.bind)
	sa_metadata.metadata.create_all(s.bind)

