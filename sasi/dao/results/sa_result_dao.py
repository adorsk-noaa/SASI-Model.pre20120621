import sasi.conf.conf as conf
import sasi.sa.results.result as sa_result
import sasi.sa.compile as sa_compile
from sasi.habitat.cell import Cell
from sasi.habitat.feature import Feature
from sasi.habitat.habitat_type import Habitat_Type
from sasi.habitat.substrate import Substrate
from sasi.fishing.gear import Gear
from sasi.results.result import Result

from sqlalchemy import func
from sqlalchemy.orm import aliased

import sys

class SA_Result_DAO(object):

	def __init__(self, session=None):
		self.session = session

	def get_results(self, filters=None):
		q = self.get_results_query(filters=filters)
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

	def delete_results(self, filters=None):
		q = self.get_results_query(query_opts=query_opts)
		q.delete()
		self.session.commit()
	
	def get_results_query(self, filters=None):
		q = self.session.query(Result)

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
					attr_code = "getattr(Result, f['attr'])"
					value_code = "f['value']"

				# Assemble filter.
				filter_code = "q = q.filter(%s%s(%s))" % (attr_code, op_code, value_code)
				if join_code: filter_code += ".%s" % join_code

				
				# Compile and execute filter code to create filter.
				compiled_filter_code = compile(filter_code, '<query>', 'exec')
				exec compiled_filter_code

		# Return query.
		return q

	# Get field values by cell, time, and field.
	def get_values_by_t_c_f(self, filters=None):

		# Initialize dictionary to hold values by cell, time, field.
		t_c_f = {}

		# Get aliased subquery for selecting filtered results.
		bq = aliased(Result, self.get_results_query(filters=filters).subquery())

		# Get field values, grouped by cell, time and field.		
		value_sum = func.sum(bq.value).label('value_sum')
		q = self.session.query(bq.time, bq.field, Cell, value_sum)
		q = q.join(Cell)
		q = q.group_by(bq.time).group_by(bq.field).group_by(Cell)

		# Assemble results into c_t dictionary.
		for row in q.all():
			t_c_f.setdefault(row.time, {})
			t_c_f[row.time].setdefault(row.Cell, {})
			t_c_f[row.time][row.Cell][row.field] = row.value_sum

		return t_c_f

	# Get a mapserver data query string.
	def get_mapserver_data_string(self, filters=None, srid=4326):

		# Get base query as subquery.
		bq = aliased(Result, self.get_results_query(filters=filters).subquery())

		# Define labeled query components.
		# NOTE: select geometry as 'RAW' in order to override default 'AsBinary'.
		value_sum = func.sum(bq.value).label('value_sum')
		geom = Cell.geom.RAW.label('geom')
		geom_id = Cell.id.label('geom_id')

		# Get value_sum, cell id, cell geometry, grouped by cell.
		q = self.session.query(value_sum, geom, geom_id).join(Cell)
		q = q.group_by(geom_id)

		# Get raw sql for query.
		q_raw_sql = sa_compile.query_to_raw_sql(q)

		# Add query into mapserver data string.
		mapserver_data_str = "geom from (%s) AS subquery USING UNIQUE geom_id USING srid=%s" % (q_raw_sql, srid)

		return mapserver_data_str

		


		


