from sqlalchemy.orm import sessionmaker

import sasi.sqlalchemy.engine as sa_engine

def get_session():
	Session = sessionmaker(bind=sa_engine.get_engine())
	return Session()
