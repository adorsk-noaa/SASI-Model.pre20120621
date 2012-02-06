from sqlalchemy import create_engine
import sasi.conf.conf as conf

def get_engine():
	return create_engine(conf.conf['db_uri'])
