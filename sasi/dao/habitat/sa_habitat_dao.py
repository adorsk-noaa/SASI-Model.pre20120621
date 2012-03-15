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

		# Define minimal base query.
		bq = self.get_filtered_query(filters=filters)
		bq = self.query_add_class(bq, Habitat_Type)
		bq_ht_alias = self.get_class_alias(bq, Habitat_Type)
		bq = bq.with_entities(bq_ht_alias.id.label('id')).subquery()

		# Get necessary aliases.
		ht_alias = aliased(Habitat_Type)
		substrate_alias = aliased(Substrate)

		# Select related substrates.
		q = self.session.query(substrate_alias).join(ht_alias).join(bq, bq.c.id == ht_alias.id).group_by(substrate_alias)

		return q.all()


	# Get energys for given habitats.
	def get_energys_for_habitats(self, filters=None):

		# Define minimal base query.
		bq = self.get_filtered_query(filters=filters)
		bq = self.query_add_class(bq, Habitat_Type)
		bq_ht_alias = self.get_class_alias(bq, Habitat_Type)
		bq = bq.with_entities(bq_ht_alias.id.label('id')).subquery()

		# Get necessary aliases.
		ht_alias = aliased(Habitat_Type)

		# Select related habitat type energys.
		q = self.session.query(ht_alias.energy).join(bq, bq.c.id == ht_alias.id).group_by(ht_alias.energy)

		return q.all()
	
	# Get habitat types for given habitats.
	def get_habitat_types_for_habitats(self, filters=None):

		# Define minimal base query.
		bq = self.get_filtered_query(filters=filters)
		bq = self.query_add_class(bq, Habitat_Type)
		bq_ht_alias = self.get_class_alias(bq, Habitat_Type)
		bq = bq.with_entities(bq_ht_alias.id.label('id')).subquery()

		# Get necessary aliases.
		ht_alias = aliased(Habitat_Type)

		# Select related habitat types.
		q = self.session.query(ht_alias).join(bq, bq.c.id == ht_alias.id).group_by(ht_alias)

		return q.all()

	# Get features for given habitats.
	def get_features_for_habitats(self, filters=None):

		# Define minimal base query.
		bq = self.get_filtered_query(filters=filters)
		bq = self.query_add_class(bq, Habitat_Type)
		bq_ht_alias = self.get_class_alias(bq, Habitat_Type)
		bq = bq.with_entities(bq_ht_alias.id.label('id')).subquery()

		# Get necessary aliases.
		ht_alias = aliased(Habitat_Type)
		feature_alias = aliased(Feature)

		# Select related features.
		q = self.session.query(feature_alias).join(ht_alias.features, feature_alias).join(bq, bq.c.id == ht_alias.id).group_by(feature_alias)

		return q.all()

	# Get a mapserver data query string.
	def get_mapserver_data_string(self, filters=None, srid=4326):

		q = self.get_filtered_query(filters=filters)

		# Add necessary classes.
		for clazz in [Habitat_Type]: q = self.query_add_class(q, clazz) 

		# Get aliases.
		ht_alias = self.get_class_alias(q, Habitat_Type)

		# Define labeled query components.
		# NOTE: for compatibility w/ PostGIS+Mapserver, select geometry as 'RAW' and explicitly specify SRID 4326.
		geom = func.ST_SetSRID(Habitat.geom.RAW, 4326).label('hab_geom')
		geom_id = Habitat.id.label('geom_id')
		substrate_id = ht_alias.substrate_id.label('substrate_id')
		energy = ht_alias.energy.label('energy')

		# Select only the labeleld components defined above.
		q = q.with_entities(geom, geom_id, substrate_id, energy)

		# Get raw sql for query.
		q_raw_sql = sa_compile.query_to_raw_sql(q)

		# Add query into mapserver data string.
		mapserver_data_str = "hab_geom from (%s) AS subquery USING UNIQUE geom_id USING srid=%s" % (q_raw_sql, srid)

		return mapserver_data_str

	# @OVERRIDE SA_DAO.
	# Custom handling for Feature attrs, due to many-to-many joins on Habitat Types.
	def query_add_class(self, q, clazz):

		if clazz == Feature:
			self.query_add_class(q, Habitat_Type)
			ht_alias = self.get_class_alias(q, Habitat_Type)
			q = q.join(ht_alias.features)
			return super(SA_Habitat_DAO, self).query_add_class(q, Feature)
		else:
			return super(SA_Habitat_DAO, self).query_add_class(q, clazz)




