from sqlalchemy.orm import aliased
from sqlalchemy.orm.util import AliasedClass

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
