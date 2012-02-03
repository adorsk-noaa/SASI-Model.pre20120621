from sqlalchemy import create_engine
import sasi.conf

def get_engine():
	return create_engine(sasi.conf.conf['db_uri'])
