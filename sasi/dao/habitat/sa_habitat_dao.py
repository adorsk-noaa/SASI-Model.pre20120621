from sasi.dao.sa_dao import SA_DAO
from sasi.dao.habitat.habitat_dao import Habitat_DAO
import sasi.sa.compile as sa_compile

import sasi.sa.habitat.habitat_metadata as sa_habitat_metadata
from sasi.habitat.habitat import Habitat
from sasi.habitat.substrate import Substrate
from sasi.habitat.feature import Feature
from sasi.habitat.habitat_type import Habitat_Type

from sqlalchemy.sql import func
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import desc


class SA_Habitat_DAO(Habitat_DAO, SA_DAO):

	def __init__(self, session=None):

		# Create class registry for SA_DAO parent class.
		class_registry = {}
		for clazz in [Habitat, Substrate, Feature, Habitat_Type]:
			class_registry[clazz.__name__] = clazz

		SA_DAO.__init__(self, session, primary_class=Habitat, class_registry=class_registry)

	def get_habitats(self, filters=None):
		q = self.get_filtered_query(filters=filters)
		return q.all()

	# Get a mapserver data query string.
	def get_mapserver_data_string(self, filters=None, srid=4326):

		# Get base mapserver query.
		q, q_primary_alias, q_registry, q_entities = self.get_base_mapserver_query(filters=filters)

		# Register the necssary entity dependencies.
		for field in ['habitat_type.energy', 'habitat_type.substrate.id']:
			q = self.register_field_dependencies(q, q_registry, field)

		# Get specific entity aliases.
		ht_parent_str = self.get_field_parent_str('habitat_type.energy')	
		ht_alias = q_registry[ht_parent_str]

		# Define labeled query components.
		# NOTE: for compatibility w/ PostGIS+Mapserver, select geometry as 'RAW' and explicitly specify SRID 4326.
		geom = func.ST_SetSRID(q_primary_alias.geom.RAW, 4326).label('hab_geom')
		geom_id = q_primary_alias.id.label('geom_id')
		substrate_id = ht_alias.substrate_id.label('substrate_id')
		energy = ht_alias.energy.label('energy')
		area = ht_alias.energy.label('area')

		# Select only the labeleld components defined above.
		q = q.with_entities(geom, geom_id, substrate_id, energy).order_by(desc(area))

		# Get raw sql for query.
		q_raw_sql = sa_compile.query_to_raw_sql(q)

		# Add query into mapserver data string.
		mapserver_data_str = "hab_geom from (%s) AS subquery USING UNIQUE geom_id USING srid=%s" % (q_raw_sql, srid)

		return mapserver_data_str


