from sqlalchemy.orm import scoped_session, sessionmaker

import sasi.sa.engine as sa_engine

def get_session():
	Session = scoped_session(sessionmaker(bind=sa_engine.get_engine()))
	return Session()
