from sqlalchemy.orm import scoped_session, sessionmaker

import sasi.sa.engine as sa_engine

Session = scoped_session(sessionmaker(bind=sa_engine.get_engine()))

def get_session():
	return Session()

def close_session():
	Session.remove()
