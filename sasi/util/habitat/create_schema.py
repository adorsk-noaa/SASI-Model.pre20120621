import sasi.sa.session as sa_session
import sasi.sa.metadata as sa_metadata
import sasi.sa.habitat.habitat as sa_habitat
import sasi.sa.habitat.cell as sa_cell
import sasi.sa.habitat.feature as sa_feature
import sasi.sa.habitat.substrate as sa_substrate

from sqlalchemy import func, MetaData
from geoalchemy import *
from geoalchemy.functions import functions as geo_func
from geoalchemy.geometry import Geometry

def main():
	create_schema()

def create_schema():

	# Get db session.
	session = sa_session.get_session()

	# Drop/Add tables
	print "Resetting db schema"

	sa_metadata.metadata.drop_all(bind = session.connection())
	sa_metadata.metadata.create_all(bind = session.connection())
	session.commit()

if __name__ == '__main__': main()
