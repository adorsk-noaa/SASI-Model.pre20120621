from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, mapper
from geoalchemy import *
from geoalchemy.postgis import PGComparator

from sasi.habitat.habitat import Habitat
from sasi.habitat.substrate import Substrate
from sasi.habitat.feature import Feature

import sasi.sa.habitat.substrate as sa_substrate
import sasi.sa.habitat.feature as sa_feature

metadata = MetaData()

habitats_features_table = Table('habitats_features', metadata,
		Column('habitat_id', Integer, ForeignKey('habitat.id')),
		Column('feature_id', String, ForeignKey(sa_feature.table.c.id))
		)

table = Table('habitat', metadata,
		Column('id', Integer, primary_key=True),
		Column('id_km100', String),
		Column('id_km1000', String),
		Column('id_vor', String),
		Column('z', Integer),
		Column('substrate_id', String, ForeignKey(sa_substrate.table.c.id)),
		Column('feature_id', String, ForeignKey(sa_feature.table.c.id)),
		Column('energy', String),
		Column('area', Float),
		GeometryExtensionColumn('geom', MultiPolygon(2)),
		Column('km100_percent', Float),
		Column('km1000_percent', Float),
		)


GeometryDDL(table)
		
mapper(Habitat, table, properties = {
	'geom': GeometryColumn(table.c.geom, comparator=PGComparator),
	'substrate': relationship(Substrate, cascade=''),
	'features': relationship(Feature, cascade='', secondary=habitats_features_table)
	})
