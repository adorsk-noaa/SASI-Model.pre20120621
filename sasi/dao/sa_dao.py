from sqlalchemy.orm import aliased, class_mapper
from sqlalchemy.orm.util import AliasedClass
from sqlalchemy.orm.properties import RelationshipProperty
from sqlalchemy.sql import func
from collections import OrderedDict
import sasi.sa.compile as sa_compile

class SA_DAO(object):

	def __init__(self, session=None, primary_class=None, class_registry=None):
		self.session = session
		self.primary_class = primary_class
		self.class_registry = class_registry

	# Get filtered query.
	def get_filtered_query(self, q=None, filters=None):

		# Initialize query with primary class, if no initial query was given.
		if not q:
			q = self.session.query(self.primary_class)

		# Handle filters.
		if filters:

			for f in filters:

				# Default operator is 'in'.
				if not f.has_key('op'): f['op'] = 'in'

				attr_code = ""
				op_code = ""
				value_code = ""

				# Handle operators.
				if f['op'] == 'in':
					op_code = '.in_'
				else:
					op_code = " %s " % f['op']

				# Handle plain attributes.
				if '.' not in f['attr']:
					f['attr'] = "%s.%s" % (self.primary_class.__name__, f['attr'])

				# Split into parts.
				parts = f['attr'].split('.')

				# Register the chain of classes with the query.
				q = self.register_attr_chain(q, f['attr'])

				# Get alias for attribute's direct class.
				clazz = self.class_registry.get(parts[-2])
				class_alias = self.get_class_alias(q, clazz)

				# Add filter for attr on last class.
				attr_code = "class_alias.%s" % parts[-1]
				value_code = "f['value']"
				filter_code = "q = q.filter(%s%s(%s))" % (attr_code, op_code, value_code)
				compiled_filter_code = compile(filter_code, '<query>', 'exec')
				exec compiled_filter_code

		# Return query.
		return q

	# Register classes from an attribute chain as given in a filter.
	def register_attr_chain(self, q, attr):

		# Split attr chain into parts.
		parts = attr.split('.')

		# For each class in the chain, if query does not yet have the class, 
		# add the class via a join.
		for i in range(len(parts) - 1):

			p = parts[i]
			clazz = self.class_registry.get(p)

			if not self.query_has_class(q, clazz):
				q = self.query_add_class(q, clazz)
		return q

	# Add a class to a query if it is not already included.
	def query_add_class(self, q, clazz):
		if not self.query_has_class(q, clazz):
			alias = aliased(clazz)
			return q.join(alias)
		return q

	# Determine if a query already includes class.
	def query_has_class(self, q, clazz):

		if clazz == self.primary_class: return True

		# Search for existing alias in query's join entities.
		for entity in q._join_entities:
			if isinstance(entity, AliasedClass):

				# If the query already has the class as an alias, return true.
				if clazz == entity._AliasedClass__target:
					return True

		# If no alias was found, return false.
		return False


	# Get the alias for an included class.
	def get_class_alias(self, q, clazz):

		# If the class is the base class, then return the plain base class.
		if clazz == self.primary_class: return self.primary_class

		# Search for existing alias in query's join entities.
		for entity in q._join_entities:
			if isinstance(entity, AliasedClass):

				# If the query already has the class as an alias, return the alias.
				if clazz == entity._AliasedClass__target:
					return entity
	

	# Get a mapserver connection string.
	def get_mapserver_connection_string(self):

		# Get engine associated with the session.
		engine = self.session.bind.engine

		# Map mapserver connection parts to SA's url elements.
		mapserver_to_sa = {
				"host": "host",
				"dbname" : "database",
				"user": "username",
				"password": "password",
				"port": "port"
				}

		# Add connection parts if present.
		connection_parts = []
		for ms_name, sa_name in mapserver_to_sa.items():
			sa_value = getattr(engine.url, sa_name)
			if sa_value: connection_parts.append("%s=%s" % (ms_name, sa_value))

		# Return the combined connection string.
		return " ".join(connection_parts)

	# Get relationships between two classes.
	def get_class_relationships(self, c1, c2):
		relationships = []
		for prop in class_mapper(c1).iterate_properties:
			if isinstance(prop, RelationshipProperty):
				if prop.mapper.class_ == c2:
					relationships.append(prop)
	
	# Get statistics.
	def get_stats(self, fields=[], grouping_fields=[], filters=None):

		# Stat functions.
		stat_funcs = {
				"count": func.count,
				"sum": func.sum,
				"avg": func.avg,
				"min": func.min,
				"max": func.max,
				"stddev": func.stddev,
				}

		# Get base query.
		bq = self.get_filtered_query(filters=filters)

		# Initialize set of entities for the base query.
		bq_entities = set()

		# Initialize list of entities for the main query.
		q_entities = set()

		# Initialize ordered dictionary of classes to be joined to the main query.
		q_class_registry = OrderedDict()

		# Initialize set of joins to add to the base query.
		joins = []

		for field in fields + grouping_fields:
			parts = field.split('.')

			for i in range(len(parts) - 1):

				p = parts[i]
				clazz = self.class_registry.get(p)

				# If class is not yet slated for the main query...
				if not q_class_registry.has_key(clazz):

					# Add the aliased class to the ordered registry.
					q_class_registry[clazz] = aliased(clazz)

					# If the class is related to the primary class...
					relations_to_primary = self.get_class_relationships(self.primary_class, clazz)
					if relations_to_primary:
						for r in relations_to_primary: 

							# Get relationship entity pairs.
							for lrp in r.local_remote_pairs:

								# Add to base query entities.
								bq_entities.add(lrp[0])

								# Add to joins.
								# (aliased_class, primary_class_column_name, aliased_class_column_name)
								joins.append({
									'type': 'bq',
									'parameters': [q_class_registry[clazz], lrp[0].name, lrp[1].name]
									})

					# Otherwise if the class is the primary class...
					if clazz == self.primary_class:
						# Add join on primary class id to joins.
						# @TODO: NEED TO ALTER THIS TO HANDLE COMPLEX PRIMARY KEYS...
						joins.append({
							'type': 'bq',
							'parameters': [q_class_registry[clazz], 'id', 'id']
							})
						bq_entities.add(self.primary_class.id)

					# Otherwise do a normal join if the class is unrelated to the primary class, and not the primary class.
					else:
						joins.append({
							'type': 'normal',
							'parameters': [q_class_registry[clazz]]
							})


		# If there were no entities, add the primary class the bq entities.
		if not bq_entities: bq_entities.add(self.primary_class)

		# Limit base query to only the required entities.
		bq = bq.with_entities(*bq_entities)
		bq = bq.subquery()

		# Create the main query.
		q = self.session.query(bq)

		# Add necessary joins.
		for j in joins:

			params = j['parameters']
			# Handle joins to the base query.
			if j['type'] == 'bq':
				q = q.join(params[0], bq.c[params[1]] == getattr(params[0], params[2]))

			# Handle other joins.
			else:
				q = q.join(params[0])


		# Add stat fields to query entities.
		for field in fields:
			parts = field.split('.')
			field_class = self.class_registry.get(parts[-2])
			field_class_alias = q_class_registry.get(field_class)
			field_e = getattr(field_class_alias, parts[-1])

			# Make individual entities for each stat function.
			for func_name, stat_func in stat_funcs.items():
				stat_e = stat_func(field_e).label("%s.%s.%s" % (parts[-2], parts[-1], func_name))
				q_entities.add(stat_e)

		# Add grouping fields to query entities, and to group by.
		for field in grouping_fields:
			parts = field.split('.')
			field_class = self.class_registry.get(parts[-2])
			field_class_alias = q_class_registry.get(field_class)
			field_e = getattr(field_class_alias, parts[-1])
			q_entities.add(field_e)
			q = q.group_by(field_e)

		# Only select required entities.
		q = q.with_entities(*q_entities)

		print sa_compile.query_to_raw_sql(q)

