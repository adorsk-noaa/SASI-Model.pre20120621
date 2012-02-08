import sasi.sa.session as sa_session
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

	# Combine tables into one metadata
	# in order to resolve dependencies.
	combined_metadata = MetaData()
	for m in [sa_cell, sa_habitat, sa_feature, sa_substrate]:
		for t in m.metadata.tables.values():
			new_t = t.tometadata(combined_metadata)

			# Run DDL if table has geometry columns.
			has_geom = False
			for c in new_t.columns:
				if isinstance(c.type, Geometry): has_geom = True
			if has_geom: GeometryDDL(new_t)

	combined_metadata.drop_all(bind = session.connection())
	combined_metadata.create_all(bind = session.connection())
	session.commit()

if __name__ == '__main__': main()
