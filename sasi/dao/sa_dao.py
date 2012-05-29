from sqlalchemy.orm import aliased, class_mapper, join
from sqlalchemy.orm.util import AliasedClass
from sqlalchemy.orm.properties import RelationshipProperty
from sqlalchemy.sql import func, asc
from collections import OrderedDict
import sasi.sa.compile as sa_compile
import copy
import re

from sqlalchemy import cast, String

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
		# @TODO: CHANGE FILTERS TO USE FIELD OBJECTS, RATHER THAN JUST IDS.  THIS WILL ALLOW FOR TRANSFORMS.
		if filters:
			for f in filters:

				# Default operator is 'in'.
				if not f.has_key('op'): f['op'] = 'in'

				# Register field dependencies.
				q = self.register_field_dependencies(q, q_registry, f['field'])

				# Get field's entity.
				field_entity = self.get_field_entity(q_registry, {'id': f['field'], 'transform': f.get('transform', None)})

				# Handle operators which for specific comparators exist.
				if self.comparators.has_key(f['op']):
					op = getattr(field_entity, self.comparators.get(f['op']))
					q = q.filter(op(f['value']))

				# Handle all other operators.
				else:
					q = q.filter(field_entity.op(f['op'])(f['value']))

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

			# Handle histogram fields.
			if field.get('as_histogram', False):

				q, bucket_label_entity = self.add_bucket_field_to_query(q, q_entities, field, field_entity)
				q = q.group_by(bucket_label_entity)

			# Handle other fields.
			else:
				q_entities.add(field_entity)
				q = q.group_by(field_entity)

				# If grouping field has a label field, add it.
				if field.has_key('label_field'):
					label_field_entity = self.get_field_entity(q_registry, field['label_field'])
					q_entities.add(label_field_entity)
					q = q.group_by(label_field_entity)

		# Only select required entities.
		q = q.with_entities(*q_entities)

		return q

	# Helper function for creating aggregate field labels.
	def get_aggregate_label(self, field_label, func_name):
		return "{}--{}".format(field_label, func_name)

	def get_aggregates(self, fields=[], grouping_fields=[], **kwargs):

		# Set default aggregate functions on fields.
		for field in fields:
			field.setdefault('aggregate_funcs', ['sum'])
			field.setdefault('label', field['id'])
	
		# Set default labels and label fields on grouping fields if not set.
		gf_counter = 0
		for grouping_field in grouping_fields:
			gf_counter += 1
			grouping_field.setdefault('label', "gf{}".format(gf_counter))
			grouping_field.setdefault('label_type', 'alpha')
			# Handle non-histogram grouping fields.
			if not grouping_field.get('as_histogram', False):
				grouping_field.setdefault('label_field', {'id': grouping_field['id']})
				grouping_field['label_field'].setdefault('label', "{}--label".format(grouping_field['label']))

		# Generate values for grouping fields which are configured to
		# include all values, with labels.
		grouping_field_values = {}
		for grouping_field in grouping_fields:
			values = []
			if grouping_field.get('all_values', False):
				for v in self.get_field_values([grouping_field]):
					if grouping_field.get('as_histogram', False):
						label = v[grouping_field['label']]
					else:
						label = v[grouping_field['label_field']['label']]
					values.append({
						'id': v[grouping_field['label']],
						'label': label,
						'label_type': grouping_field['label_type']
						})
			grouping_field_values[grouping_field['id']] = values 

		# Get aggregate results as dictionaries.
		rows = self.get_aggregates_query(fields=fields, grouping_fields=grouping_fields, **kwargs).all()
		aggregates = [dict(zip(row.keys(), row)) for row in rows]

		# Initialize result tree with aggregates.
		result_tree = {'label': '', 'id': 'root'}
		for aggregate in aggregates:
			current_node = result_tree
			for grouping_field in grouping_fields:

				# Initialize children if not yet set.
				if not current_node.has_key('children'):
					current_node['children'] = {}
					for value in grouping_field_values.get(grouping_field['id'], []):
						current_node['children'][value['id']] = {'label': value['label'], 'id': value['id']}

				# Set current node to next tree node (initializing if not yet set).
				current_node = current_node['children'].setdefault(aggregate[grouping_field['label']], {})
				current_node['id'] = aggregate[grouping_field['label']]
				if not grouping_field.get('as_histogram', False):
					label = grouping_field['label_field']['label']
				else:
					label = grouping_field['label']
				current_node['label'] = aggregate[label]
				current_node['label_type'] = grouping_field['label_type']

			# We should now be at a leaf. Set leaf's data.
			#current_node['label'] = aggregate[grouping_field['label_field']['label']]
			#current_node['id'] = aggregate[grouping_field['label']]
			current_node['data'] = []
			for field in fields:
				for func_name in field['aggregate_funcs']:
					aggregate_label = self.get_aggregate_label(field['label'], func_name)
					current_node['data'].append({
						'label': aggregate_label,
						'value': aggregate.get(aggregate_label)
						})


		# Set default values for unvisited leafs.
		default_value = []
		for field in fields: 
			for func_name in field['aggregate_funcs']:
				aggregate_label = self.get_aggregate_label(field['label'], func_name)
				default_value.append({
					'label': aggregate_label,
					'value': 0
					})

		# Process tree recursively to set values on unvisited leafs and calculate branch values.
		self._process_aggregates_tree(result_tree, default_value_func=lambda: copy.deepcopy(default_value))

		# Merge in aggregates for higher grouping levels (if any).
		if len(grouping_fields) > 0:
			parent_tree = self.get_aggregates(fields=fields, grouping_fields=grouping_fields[:-1], **kwargs)
			self._merge_aggregates_trees(parent_tree, result_tree)

		return result_tree

	# Helper function to recursively process aggregates result tree.
	def _process_aggregates_tree(self, node, default_value_func=None):
		if node.has_key('children'):
			for child in node['children'].values():
				self._process_aggregates_tree(child, default_value_func)
		else:
			# Set default value on node if it's blank.
			if not node.has_key('data') and default_value_func: node['data'] = default_value_func()
	
	# Helper function to recursively merge tree1 into tree2.
	# Modifies tree2 in-place.
	def _merge_aggregates_trees(self, node1, node2):
		if node1.has_key('children'):
			for child_key in node1['children'].keys():
				self._merge_aggregates_trees(node1['children'][child_key], node2.setdefault('children',{}).setdefault(child_key,{}))
		node2['data'] = node1['data']

	def get_field_min_max(self, field, filters=[]):
		simple_field = { 'id': field.get('id') , 'transform': field.get('transform')}
		simple_field['aggregate_funcs'] = ['min', 'max']
		aggregates = self.get_aggregates(fields=[simple_field], filters=filters)
		field_min = float(aggregates['data'][0]['value'])
		field_max = float(aggregates['data'][1]['value'])
		return field_min, field_max

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

		entities = {}

		# Legacy hack, for temporary backwards compatibility.
		field.setdefault('template', "{{field:{}}}".format(field['id']))

		# Set default label on field, if not provided..
		field.setdefault('label', field['template'])

		# Replace fields w/ entities.
		def replace_with_entity(m):
			field_id = m.group(1)
			parent = registry.get(self.get_field_parent_str(field_id))
			parts = field_id.split('.')
			field_entity = getattr(parent,parts[-1])
			entities[field_id] = field_entity
			return "entities['{}']".format(field_id)

		entity_code = re.sub('{field:(.*?)}', replace_with_entity, field['template'])

		# Evaluate and label.
		field_entity = eval(entity_code)
		field_entity = field_entity.label(field['label'])

		return field_entity
	

	# Select values for a given set of fields.
	def get_field_values(self, fields, as_dicts=True):

		# Initialize registry and query.
		primary_alias = aliased(self.primary_class)
		q_registry = {self.primary_class.__name__: primary_alias}
		q_entities = set()
		q = self.session.query(primary_alias)

		# Register field dependencies and get field entities.
		for field in fields:

			# If field has label field, add label field to list of fields.
			if field.get('label_field', False):
				fields.append(field['label_field'])

			q = self.register_field_dependencies(q, q_registry, field['id'])
			field_entity = self.get_field_entity(q_registry, field)

			# If field is a histogram field, get bucket entities for the field.
			if field.get('as_histogram', False):
				q, bucket_label_entity = self.add_bucket_field_to_query(q, q_entities, field, field_entity)
				q = q.group_by(bucket_label_entity)

			else:
				q_entities.add(field_entity)
				q = q.group_by(field_entity)
				
			q = q.with_entities(*q_entities)

		rows = q.all()

		# Return field values
		if as_dicts:
			return [dict(zip(row.keys(), row)) for row in rows]
		else: 
			return rows
	

	# Add bucket entity to query.
	# Constrains buckets to given field_max. This overrides default sql behavior to make last bucket be all values >= field_max.
	def add_bucket_field_to_query(self, q, q_entities, field, field_entity):
		# Get min, max if not provided.
		field_min = 0
		field_max = 0

		if (not field.has_key('min') or not field.has_key('max')):
			field_min, field_max = self.get_field_min_max(field)

		# Override calculated min/max if values were provided.
		if field.has_key('min'): field_min = field.get('min')
		if field.has_key('max'): field_max = field.get('max')

		num_buckets = field.get('num_buckets', 10)

		# Get bucket width.
		bucket_width = (field_max - field_min)/num_buckets

		# Get bucket field entities.
		# Bit of a trick here: we use field_max - bucket_width because normally last bucket gets all values >= field_max.
		# Here we use one less bucket, and then filter.  This essentially makes the last bucket include values <= field_max.
		bucket_entity = func.width_bucket(field_entity, field_min, field_max - bucket_width, num_buckets - 1)
		q = q.filter(field_entity <= field_max)
		bucket_label_entity = (cast(field_min + (bucket_entity - 1) * bucket_width, String) + ' to ' + cast(field_min + bucket_entity * bucket_width, String))
		bucket_label_entity = bucket_label_entity.label(field['label'])

		q_entities.add(bucket_label_entity)
		return q, bucket_label_entity


	def get_base_mapserver_query(self, filters):

		# Get base query as subquery, and select only the primary class id.
		bq_primary_alias = aliased(self.primary_class)
		bq = self.get_filtered_query(primary_alias=bq_primary_alias, filters=filters).with_entities(bq_primary_alias.id)
		bq = bq.subquery()

		# Initialize primary class alias and registry for main query.
		q_primary_alias = aliased(self.primary_class)
		q_registry = {self.primary_class.__name__: q_primary_alias}

		# Create the main query, and join the basequery on the primary class id.
		q = self.session.query(q_primary_alias).join(bq, q_primary_alias.id == bq.c.id)

		# Initialize list of entities for the main query.
		q_entities = set()

		return q, q_primary_alias, q_registry, q_entities


