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

	# Get substrates for given habitats.
	def get_substrates_for_habitats(self, filters=None):

		bq = self.get_aggregates_query(fields=['habitat_type.substrate.id'], grouping_fields=['habitat_type.substrate.id'], filters=filters).subquery()
		substrate_alias = aliased(Substrate)
		q = self.session.query(substrate_alias).join(bq, substrate_alias.id == bq.c.id)
		return q.all()

	# Get energys for given habitats.
	def get_energys_for_habitats(self, filters=None):

		q = self.get_aggregates_query(fields=['habitat_type.energy'], grouping_fields=['habitat_type.energy'], filters=filters)
		return [row[0] for row in q.all()]
	
	# Get habitat types for given habitats.
	def get_habitat_types_for_habitats(self, filters=None):

		bq = self.get_aggregates_query(fields=['habitat_type.id'], grouping_fields=['habitat_type.id'], filters=filters).subquery()
		ht_alias = aliased(Habitat_Type)
		q = self.session.query(ht_alias).join(bq, ht_alias.id == bq.c.id)
		return q.all()

	# Get features for given habitats.
	def get_features_for_habitats(self, filters=None):

		bq = self.get_aggregates_query(fields=['habitat_type.features.id'], grouping_fields=['habitat_type.features.id'], filters=filters).subquery()
		feature_alias = aliased(Feature)
		q = self.session.query(feature_alias).join(bq, feature_alias.id == bq.c.id)
		return q.all()

	# Get a mapserver data query string.
	def get_mapserver_data_string(self, filters=None, srid=4326):

		# Get base query as subquery, and select only the primary class id.
		bq_primary_alias = aliased(self.primary_class)
		bq = self.get_filtered_query(primary_alias=bq_primary_alias, filters=filters).with_entities(bq_primary_alias.id)
		bq = bq.subquery()

		# Initialize primary class alias and registry for main query.
		q_primary_alias = aliased(self.primary_class)
		q_registry = {self.primary_class.__name__: q_primary_alias}

		# Initialize list of entities for the main query.
		q_entities = set()

		# Create the main query, and join the basequery on the primary class id.
		q = self.session.query(q_primary_alias).join(bq, q_primary_alias.id == bq.c.id)

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

		# Select only the labeleld components defined above.
		q = q.with_entities(geom, geom_id, substrate_id, energy)

		# Get raw sql for query.
		q_raw_sql = sa_compile.query_to_raw_sql(q)

		# Add query into mapserver data string.
		mapserver_data_str = "hab_geom from (%s) AS subquery USING UNIQUE geom_id USING srid=%s" % (q_raw_sql, srid)

		return mapserver_data_str


