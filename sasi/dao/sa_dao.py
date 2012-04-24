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
					'intersects': 'intersects',
					}

	# Get filtered query.
	def get_filtered_query(self, primary_alias=None, filters=None):

		# If no alias was given, registry with aliased primary class.
		if not primary_alias:
			primary_alias = aliased(self.primary_class)

		# Initialize registry and query.
		q_registry = {self.primary_class.__name__: primary_alias}
		q = self.session.query(primary_alias).distinct(primary_alias.id)

		# Handle filters.
		if filters:
			for f in filters:

				# Default operator is 'in'.
				if not f.has_key('op'): f['op'] = 'in'

				# Register field dependencies.
				q = self.register_field_dependencies(q, q_registry, f['field'])

				# Get field's entity.
				field = self.get_field_entity(q_registry, {'id': f['field']})

				# Get operator function.

				# Handle operators which for specific comparators exist.
				if self.comparators.has_key(f['op']):
					op = getattr(field, self.comparators.get(f['op']))
					q = q.filter(op(f['value']))

				# Handle all other operators.
				else:
					q = q.filter(field.op(f['op'])(f['value']))

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

	
	# Get aggregates query.
	# Note: this assumes that the primary_class has a single 'id' field for joining.
	def get_aggregates_query(self, fields=[], grouping_fields=[], filters=None):

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
			q = self.register_field_dependencies(q, q_registry, field['id'])

		# Add labeled stat fields to query entities.
		for field in fields:

			field_entity = self.get_field_entity(q_registry, field)

			# Set default aggregate functions.
			field.setdefault('aggregate_funcs', ['sum'])

			# Make individual entities for each aggregate function.
			for func_name in field['aggregate_funcs']:
				aggregate_func = getattr(func, func_name)
				aggregate_entity = aggregate_func(field_entity)
				if field.has_key('label'): label = field['label']
				else: label = field['id']
				aggregate_label = self.get_aggregate_label(field['label'], func_name)
				aggregate_entity = aggregate_entity.label(aggregate_label)
				q_entities.add(aggregate_entity)

		# Add grouping fields to query entities, and to group by.
		for field in grouping_fields:
			field_entity = self.get_field_entity(q_registry, field)
			q_entities.add(field_entity)
			q = q.group_by(field_entity)

		# Only select required entities.
		q = q.with_entities(*q_entities)

		return q

	# Helper function for creating aggregate field labels.
	def get_aggregate_label(self, field_label, func_name):
		return "{}--{}".format(field_label, func_name)

	def get_aggregates(self, as_dicts=True, fields=[], grouping_fields=[], **kwargs):
		# Set default aggregate functions on fields.
		for field in fields:
			field.setdefault('aggregate_funcs', ['sum'])
	
		# Generate result templates for grouping fields which are configured to
		# include all values.
		result_templates = {}
		for grouping_field in grouping_fields:
			if grouping_field.get('all_values', False):
				result_templates[grouping_field['id']] = self.get_field_values(grouping_field)

		# Get aggregate results as dictionaries.
		rows = self.get_aggregates_query(fields=fields, grouping_fields=grouping_fields, **kwargs).all()
		aggregates = [dict(zip(row.keys(), row)) for row in rows]

		# Make list of value fields (per aggregate query convention).

		# Initialize result tree with aggregates.
		result_tree = {}
		for aggregate in aggregates:
			current_node = result_tree
			for grouping_field in grouping_fields:

				# Initialize children if not yet set.
				if not current_node.has_key('children'):
					current_node['children'] = {}
					for value in result_templates.get(grouping_field['id'], []):
						current_node['children'][value] = {}

				# Set current node to next tree node (initializing if not yet set).
				current_node = current_node['children'].setdefault(aggregate[grouping_field['label']], {})

			# We should now be at a leaf. Set leaf's data.
			current_node['data'] = {}
			for field in fields:
				for func_name in field['aggregate_funcs']:
					aggregate_label = self.get_aggregate_label(field['label'], func_name)
					current_node['data'][aggregate_label] = aggregate[aggregate_label]


		# Set default values for unvisited leafs.
		default_value = {}
		for field in fields: 
			for func_name in field['aggregate_funcs']:
				aggregate_label = self.get_aggregate_label(field['label'], func_name)
				default_value[aggregate_label] = 0

		# Process tree recursively to set values on unvisited leafs and calculate branch values.
		self._process_aggregates_tree(result_tree, default_value)

		return result_tree

	# Helper function to recursively process aggregates result tree.
	def _process_aggregates_tree(self, node, default_value=None):
		if node.has_key('children'):
			for child in node['children'].values():
				self._process_aggregates_tree(child, default_value)
		else:
			# Set default value on node if it's blank.
			if not node.has_key('data'): node['data'] = default_value


	# Get histogram.
	# Note: this assumes that the primary_class has a single 'id' field for joining.
	def get_histogram(self, bucket_field=None, field_min=None, field_max=None, num_buckets=10, grouping_fields=[], filters=None):

		# Set label on bucket field if not set.
		if not bucket_field.has_key('label'): bucket_field['label'] = bucket_field['id']

		# If min and max were not given, get them.
		if not field_min or not field_max:
			aggregates = self.get_aggregates(fields=[bucket_field], aggregate_funcs=['min','max'], filters=filters).pop()
			field_max = float(aggregates["%s--max" % bucket_field['label']])
			field_min = float(aggregates["%s--min" % bucket_field['label']])

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
		for field in [bucket_field] + grouping_fields:
			q = self.register_field_dependencies(q, q_registry, field['id'])

		# Add grouping fields to query entities, and to group by.
		for field in grouping_fields:
			field_entity = self.get_field_entity(q_registry, field)
			q_entities.add(field_entity)
			q = q.group_by(field_entity)

		# Create bucket field entity.
		bucket_field_entity = self.get_field_entity(q_registry, bucket_field)

		# Explicitly count values which == field_max.
		num_max_values = 0
		max_count_entity = func.count(q_primary_alias.id).label('max_count')
		max_count_q_entities = list(q_entities) + [max_count_entity]
		max_count = q.filter(bucket_field_entity == field_max).with_entities(*max_count_q_entities).one()[0]

		# Create bucket entity.
		bucket_entity = func.width_bucket(bucket_field_entity, field_min, field_max, num_buckets).label('bucket')
		q_entities.add(bucket_entity)

		# Add labeled count field to query entities.
		count_entity = func.count(q_primary_alias.id).label('bucket_count')
		q_entities.add(count_entity)

		# Add bucket entity to group by.
		q = q.group_by(bucket_entity)

		# Only select required entities.
		q = q.with_entities(*q_entities)

		# Calculate bucket width.
		bucket_width = (field_max - field_min)/num_buckets

		# Format results.
		buckets = []
		rows = q.all()
		row_dicts = [dict(zip(row.keys(), row)) for row in rows]
		for r in row_dicts:
			buckets.append({
				'bucket': r['bucket'],
				'min': field_min + (r['bucket'] - 1) * bucket_width,
				'max': field_min + (r['bucket']) * bucket_width,
				'count': r['bucket_count'],
				})
		buckets.sort(key=lambda b: b['min'])

		# Last bucket is values >= field_max.  We want the values that == field_max to go in the 2nd to last bucket.
		if len(buckets) >= 2:
			buckets[-2]['count'] += max_count

		# Remove the last bucket.
		buckets.pop()

		return buckets
 

	def register_field_dependencies(self, q, registry, field_id):

		# Process field dependencies, from left to right.
		parts = field_id.split('.')
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

	def get_field_entity(self, registry, field):
		parent = registry.get(self.get_field_parent_str(field['id']))
		parts = field['id'].split('.')
		field_entity = getattr(parent,parts[-1])

		if field.has_key('transform'):
			transform_code = field['transform'].format(field = 'field_entity')
			exec compile("field_entity = {0}".format(transform_code), '<field_entity>', 'exec')

		if field.has_key('label'):
			return field_entity.label(field['label'])
		else: return field_entity
	

	# Select values for a given field.
	def get_field_values(self, field):

		# Initialize registry and query.
		primary_alias = aliased(self.primary_class)
		q_registry = {self.primary_class.__name__: primary_alias}
		q = self.session.query(primary_alias)

		# Register field dependencies.
		q = self.register_field_dependencies(q, q_registry, field['id'])

		# Get field's entity.
		field_entity = self.get_field_entity(q_registry, field)

		# Select only the field entity.
		q = q.group_by(field_entity).with_entities(field_entity)

		# Return field values
		return [r[0] for r in q.all()]




