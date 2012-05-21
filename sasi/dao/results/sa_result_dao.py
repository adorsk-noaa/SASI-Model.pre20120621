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
	def get_mapserver_data_string(self, filters=None, srid=4326):

		# Get base query as subquery.
		bq = aliased(Result, self.get_filtered_query(filters=filters).subquery())

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

		


		


