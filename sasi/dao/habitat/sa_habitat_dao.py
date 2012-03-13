from sasi.dao.habitat.habitat_dao import Habitat_DAO
import sasi.sa.session as sa_session
import sasi.dao.sa as sa_dao
import sasi.sa.compile as sa_compile
import sasi.sa.habitat.habitat_metadata as sa_habitat_metadata
from sasi.habitat.habitat import Habitat
from sasi.habitat.substrate import Substrate
from sasi.habitat.feature import Feature
from sasi.habitat.habitat_type import Habitat_Type

from sqlalchemy.orm import aliased
from sqlalchemy.sql import func


class SA_Habitat_DAO(Habitat_DAO):

	def __init__(self, session=None):
		self.session = session

	def get_habitats(self, filters=None):

		# Get filtered query.
		q = self.get_filtered_query(filters=filters)

		return q.all()

	# Get filtered query for habitats.
	def get_filtered_query(self, q=None, filters=None):

		# Initialize base query.
		if not q:
			q = self.session.query(Habitat)

		# Handle filters.
		if filters:

			# Initialize alias registry and joins list.
			alias_registry = {}
			joins_registry = {}
			ordered_joins = []

			for f in filters:

				# Default operator is 'in'.
				if not f.has_key('op'): f['op'] = 'in'

				attr_code = ""
				join_code = ""
				op_code = ""
				value_code = ""

				# Handle operators.
				if f['op'] == 'in':
					op_code = '.in_'
				else:
					op_code = " %s " % f['op']

				# Handle plain attributes.
				if '.' not in f['attr']:
					f['attr'] = "Habitat." + f['attr']

				# Split into parts.
				parts = f['attr'].split('.')

				# Register aliases for classes.

				for i in range(len(parts) - 1):

					p = parts[i]

					# 'Habitat_Type.Feature' attribute gets special handling for join,
					# since many-to-many relationships must use explicit joins.
					if p == 'Feature' and i > 0 and parts[i-1] == 'Habitat_Type':
						alias_registry['Feature'] = Feature
						ht_clazz = alias_registry['Habitat_Type']
						if not joins_registry.has_key(ht_clazz.features):
							joins_registry[ht_clazz.features] = ht_clazz.features
							ordered_joins.append(ht_clazz.features)
					else:
						# Get class for the part.
						# This will set a variable 'clazz'.
						exec compile("clazz = eval(p)", '<query>', 'exec')
						if not alias_registry.has_key(p):

							# Register aliases for non-Habitat classes.
							if not p == 'Habitat':
								alias_registry[p] = aliased(clazz)
								joins_registry[p] = alias_registry[p]
								ordered_joins.append(alias_registry[p])
							# For Habitat, use the class itelf. Otherwise the habitat table will appear twice,
							# once in the base query, and once in the filters.
							else:
								alias_registry[p] = Habitat

				# Add filter for attr on last class.
				attr_code = "alias_registry['%s'].%s" % (parts[-2], parts[-1])
				value_code = "f['value']"

				# Assemble filter.
				filter_code = "q = q.filter(%s%s(%s))" % (attr_code, op_code, value_code)

				# Compile and execute filter code to create filter.
				compiled_filter_code = compile(filter_code, '<query>', 'exec')
				exec compiled_filter_code

			# Add joins for filters.
			for j in ordered_joins:
				q = q.join(j)


		# Return query.
		return q

	# Get substrates for given habitats.
	def get_substrates_for_habitats(self, filters=None):

		# Define filtered base query.
		bq = self.get_filtered_query(q=self.session.query(Habitat_Type.substrate).join(Habitat, aliased=True), filters=filters)

		# Define base query.
		q = self.session.query(Substrate).join(bq.subquery(), aliased=True).group_by(Substrate)

		return q.all()

	# Get energies for given habitats.
	def get_energys_for_habitats(self, filters=None):

		# Define base query.
		q = self.session.query(Habitat_Type.energy).join(Habitat).group_by(Habitat_Type.energy)

		# Apply filters.
		q = self.get_filtered_query(q=q, filters=filters)

		return q.all()
	
	# Get habitat types for given habitats.
	def get_habitat_types_for_habitats(self, filters=None):

		# Define base query.
		q = self.session.query(Habitat_Type).join(Habitat).group_by(Habitat_Type)

		# Apply filters.
		q = self.get_filtered_query(q=q, filters=filters)

		return q.all()

	# Get features for given habitats.
	def get_features_for_habitats(self, filters=None):

		# Define filtered base query.
		bq = self.get_filtered_query(q=self.session.query(Habitat_Type.id).join(Habitat), filters=filters)

		# Define base query.
		q = self.session.query(Feature).join(Habitat_Type.features, bq.subquery()).group_by(Feature)

		return q.all()

	# Get a mapserver connection string.
	def get_mapserver_connection_string(self):
		return sa_dao.get_mapserver_connection_string(self)

	# Get a mapserver data query string.
	def get_mapserver_data_string(self, filters=None, srid=4326):

		# Define labeled query components.
		# NOTE: for compatibility w/ PostGIS+Mapserver, select geometry as 'RAW' and explicitly specify SRID 4326.
		geom = func.ST_SetSRID(Habitat.geom.RAW, 4326).label('hab_geom')
		geom_id = Habitat.id.label('geom_id')
		substrate_id = Habitat_Type.substrate_id.label('substrate_id')
		energy = Habitat_Type.energy.label('energy')

		# Define base query.
		q = self.session.query(geom, geom_id, substrate_id, energy).select_from(Habitat).join(Habitat_Type)

		# Apply filters.
		q = self.get_filtered_query(q=q, filters=filters)

		# Get raw sql for query.
		q_raw_sql = sa_compile.query_to_raw_sql(q)

		# Add query into mapserver data string.
		mapserver_data_str = "hab_geom from (%s) AS subquery USING UNIQUE geom_id USING srid=%s" % (q_raw_sql, srid)

		return mapserver_data_str
