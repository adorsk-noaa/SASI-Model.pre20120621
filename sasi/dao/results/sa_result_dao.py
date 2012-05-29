import sasi.conf.conf as conf
from sasi.dao.sa_dao import SA_DAO
import sasi.sa.results.result as sa_result
import sasi.sa.compile as sa_compile
from sasi.habitat.cell import Cell
from sasi.habitat.feature import Feature
from sasi.habitat.habitat_type import Habitat_Type
from sasi.habitat.substrate import Substrate
from sasi.fishing.gear import Gear
from sasi.results.result import Result

import sasi.dao.sa as sa_dao

from sqlalchemy import func
from sqlalchemy.orm import aliased


import sys

class SA_Result_DAO(SA_DAO):

	def __init__(self, session=None):

		# Create class registry for SA_DAO parent class.
		class_registry = {}
		for clazz in [Cell, Feature, Habitat_Type, Substrate, Gear, Result]:
			class_registry[clazz.__name__] = clazz

		SA_DAO.__init__(self, session, primary_class=Result, class_registry=class_registry)

	def get_results(self, filters=None):
		q = self.get_filtered_query(filters=filters)
		return q.all()

	def save_results(self, results, batch_insert=True, batch_size = 10000, commit=True):

		# We use raw sql for bulk inserts. Result sets can be large.

		# If not batching...
		if not batch_insert:
			# Map results to columns.
			mapped_results = []
			for r in results:
				mapped_results.append({
					'time': r.time,
					'cell_id': r.cell.id,
					'habitat_type_id': r.habitat_type.id,
					'gear_id': r.gear.id,
					'feature_id': r.feature.id,
					'tag': r.tag,
					'field': r.field,
					'value': r.value
					})
			# Insert.
			self.session.execute(sa_result.table.insert(), mapped_results)

		# If batching...
		else:
			# Initialize current batch.
			batch = []
			batch_counter = 1

			# For each result...
			for r in results:

				# If batch is at batch size, process the batch w/out committing.
				if (batch_counter % batch_size) == 0: 
					self.save_results(batch, batch_insert=False, commit=False)
					batch = []
					if conf.conf['verbose']: print >> sys.stderr, "Processed %s of %s results. (%.1f)%%" % (batch_counter, len(results), (1.0 * batch_counter)/len(results) * 100)

				# Add the result to the batch.
				batch.append(r)
				batch_counter += 1

			# Save any remaining batch items.
			if batch: self.save_results(batch, batch_insert=False, commit=False)


		# Commit if commit is true.
		if commit: 
			self.session.commit()
			if conf.conf['verbose']: print >> sys.stderr, "Saved %s results." % len(results)


	# Get a mapserver data query string.
	def get_mapserver_data_string(self, result_field=None, filters=[], srid=4326):

		# Create filter for selecting value field.
		result_field_filter = {
				'field': 'field',
				'op': '==',
				'value': result_field['field']
				}

		# Get base mapserver query.
		q, q_primary_alias, q_registry, q_entities = self.get_base_mapserver_query(filters= filters + [result_field_filter])

		# Create field definition for the 'value' column.
		# Note that we use density, rather than total value.
		value_field = {
				'id': 'value',
				'template': '{field:value}/{field:cell.area}',
				'aggregate_funcs': result_field.get('aggregate_funcs', ['sum'])
				}

		# Register the value field.
		q = self.register_field_dependencies(q, q_registry, value_field.get('template', '{{field:{}}}'.format(value_field['id'])))
		value_field_entity = self.get_field_entity(q_registry, value_field)

		# Make labeled entity for aggregate function.
		func_name = value_field['aggregate_funcs'][0]
		aggregate_func = getattr(func, func_name)
		aggregate_entity = aggregate_func(value_field_entity).label("value_field")
		q_entities.add(aggregate_entity)

		# Register the necssary entity dependencies.
		for field in ['{field:cell.geom}']:
			q = self.register_field_dependencies(q, q_registry, field)

		# Get specific entity aliases.
		cell_parent_str = self.get_field_parent_str('cell.id')	
		cell_alias = q_registry[cell_parent_str]

		# Define labeled query components.
		# NOTE: for compatibility w/ PostGIS+Mapserver, select geometry as 'RAW' and explicitly specify SRID 4326.
		geom = func.ST_SetSRID(cell_alias.geom.RAW, 4326).label('geom')
		geom_id = cell_alias.id.label('geom_id')

		# Select only the labeleld components defined above, grouping on cell.
		q = q.with_entities(geom, geom_id, aggregate_entity).group_by(cell_alias.id)

		# Get raw sql for query.
		q_raw_sql = sa_compile.query_to_raw_sql(q)

		# Add query into mapserver data string.
		mapserver_data_str = "geom from (%s) AS subquery USING UNIQUE geom_id USING srid=%s" % (q_raw_sql, srid)

		return mapserver_data_str

		


		


