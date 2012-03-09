import sasi.sa.session as sa_session
import sasi.sa.habitat.habitat as sa_habitat
import sasi.dao.sa as sa_dao
import sasi.sa.compile as sa_compile
from sasi.dao.habitat.habitat_dao import Habitat_DAO
from sasi.habitat.habitat import Habitat
from sasi.habitat.habitat_type import Habitat_Type

from sqlalchemy.orm import aliased
from sqlalchemy.sql import func


class SA_Habitat_DAO(Habitat_DAO):

	def __init__(self, session=None):
		self.session = session

	def get_habitats(self, filters=None):

		# Get query for filters.
		q = self.get_query(filters)

		return q.all()

	# Get query for habitats.
	def get_query(self, filters=None):

		# Initialize base query.
		q = self.session.query(Habitat)

		# Handle filters.
		if filters:
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

				# Handle attributes on related objects.
				if '.' in f['attr']:

					# Split into parts.
					parts = f['attr'].split('.')

					# Join on classes.
					join_code = '.'.join(["join(%s)" % clazz for clazz in parts[:-1]])

					# Add filter for attr on last class.
					attr_code = "%s.%s" % (parts[-2], parts[-1])
					value_code = "f['value']"

				# Handle all other attrs.
				else: 
					attr_code = "getattr(Habitat, f['attr'])"
					value_code = "f['value']"

				# Assemble filter.
				filter_code = "q = q.filter(%s%s(%s))" % (attr_code, op_code, value_code)
				if join_code: filter_code += ".%s" % join_code

				
				# Compile and execute filter code to create filter.
				compiled_filter_code = compile(filter_code, '<query>', 'exec')
				exec compiled_filter_code

		# Return query.
		return q

	# Get a mapserver connection string.
	def get_mapserver_connection_string(self):
		return sa_dao.get_mapserver_connection_string(self)

	# Get a mapserver data query string.
	def get_mapserver_data_string(self, filters=None, srid=4326):

		# Get base query as subquery.
		bq = aliased(Habitat, self.get_query(filters=filters).subquery())

		# Define labeled query components.
		# NOTE: for compatibility w/ PostGIS+Mapserver, select geometry as 'RAW' and explicitly specify SRID 4326.
		geom = func.ST_SetSRID(bq.geom.RAW, 4326).label('hab_geom')
		geom_id = bq.id.label('geom_id')
		substrate_id = Habitat_Type.substrate_id.label('substrate_id')
		energy = Habitat_Type.energy.label('energy')

		# Get habitat id, geometry, substrate type, and energy.
		q = self.session.query(geom, geom_id, substrate_id, energy).join(Habitat_Type)

		# Get raw sql for query.
		#q_raw_sql = sa_compile.query_to_raw_sql(q.with_labels())
		q_raw_sql = sa_compile.query_to_raw_sql(q)

		# Add query into mapserver data string.
		mapserver_data_str = "hab_geom from (%s) AS subquery USING UNIQUE geom_id USING srid=%s" % (q_raw_sql, srid)

		return mapserver_data_str
