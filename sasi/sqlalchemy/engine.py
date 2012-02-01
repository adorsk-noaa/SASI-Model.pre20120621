from sqlalchemy import create_engine
import sasi.conf

engine = create_engine(sasi.conf.conf['db_uri'])
