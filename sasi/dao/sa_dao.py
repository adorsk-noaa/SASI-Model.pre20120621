from sqlalchemy.orm import aliased, class_mapper, join
from sqlalchemy.orm.util import AliasedClass
from sqlalchemy.orm.properties import RelationshipProperty
from sqlalchemy.sql import func
from collections import OrderedDict
import sasi.sa.compile as sa_compile

class SA_DAO(object):

	def __init__(self, session=None, primary_class=None, class_registry=None, comparators=None):
		self.session = session
		self.primary_class = primary_class
		self.class_registry = class_registry
		if comparators:
			self.comparators = comparators
		else:
			self.comparators= {
					'==': '__eq__',
					'!=': '__ne__',
					'<': '__lt__',
					'>': '__gt__',
					'<=': '__le__',
					'>=': '__ge__',
					'in': 'in_',
					}

	# Get filtered query.
	def get_filtered_query(self, primary_alias=None, filters=None):

		# If no alias was given, registry with aliased primary class.
		if not primary_alias:
			primary_alias = aliased(self.primary_class)

		# Initialize registry and query.
		q_registry = {self.primary_class.__name__: primary_alias}
		q = self.session.query(primary_alias)

		# Handle filters.
		if filters:
			for f in filters:

				# Default operator is 'in'.
				if not f.has_key('op'): f['op'] = 'in'

				# Register field dependencies.
				q = self.register_field_dependencies(q, q_registry, f['field'])

				# Get field's entity.
				field = self.get_field_entity(q_registry, f['field'])

				# Get operator function.
				op = getattr(field, self.comparators.get(f['op']))

				# Add filter for field.
				q = q.filter(op(f['value']))

		# Return query.
		return q

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

	
	# Get aggregates.
	# Note: this assumes that the primary_class has a single 'id' field for joining.
	def get_aggregates(self, fields=[], grouping_fields=[], filters=None, aggregate_funcs = []):

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

		# Register fields and grouping fields.
		for field in fields + grouping_fields:
			q = self.register_field_dependencies(q, q_registry, field)

		# Add stat fields to query entities.
		for field in fields:

			field_entity = self.get_field_entity(q_registry, field)

			# Make individual entities for each aggregate function.
			for func_name in aggregate_funcs:
				aggregate_func = getattr(func, func_name)
				aggregate_entity = aggregate_func(field_entity).label("%s--%s" % (field, func_name))
				q_entities.add(aggregate_entity)

		# Add grouping fields to query entities, and to group by.
		for field in grouping_fields:
			field_entity = self.get_field_entity(q_registry, field)
			q_entities.add(field_entity)
			q = q.group_by(field_entity)

		# Only select required entities.
		q = q.with_entities(*q_entities)

		print sa_compile.query_to_raw_sql(q)
		#return q.all()


	def register_field_dependencies(self, q, registry, field_str):

		# Process field dependencies, from left to right.
		parts = field_str.split('.')
		for i in range(len(parts) - 1):
			parent_str = self.get_field_parent_str('.'.join(parts[:i+1]))
			dependency_str = '.'.join([parent_str, parts[i]])

			# If already registered, continue.
			if registry.has_key(dependency_str): continue

			else:
				parent =  registry.get(parent_str)
				prop = class_mapper(parent._AliasedClass__target).get_property(parts[i])
				if isinstance(prop, RelationshipProperty):
					child = aliased(prop.mapper.class_)
					registry[dependency_str] = child
					q = q.join(child, getattr(parent,parts[i]))

		return q

	def get_field_parent_str(self, field):
		parts = field.split('.')
		if (len(parts) < 2): 
			return self.primary_class.__name__
		else: 
			return '.'.join([self.primary_class.__name__] + parts[:-1])

	def get_field_entity(self, registry, field_str):
		parent = registry.get(self.get_field_parent_str(field_str))
		parts = field_str.split('.')
		return getattr(parent, parts[-1])
