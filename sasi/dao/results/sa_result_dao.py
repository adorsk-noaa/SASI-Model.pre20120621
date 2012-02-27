import sasi.sa.results.result
from sasi.habitat.cell import Cell
from sasi.results.result import Result

from sqlalchemy import func
from sqlalchemy.orm import aliased

class SA_Result_DAO(object):

	def __init__(self, session=None):
		self.session = session

	def get_results(self, filters=None):
		q = self.get_filtered_results_query(filters=filters)
		return q.all()

	def save_results(self, results, commit=True):
		self.session.add_all(results)
		if commit: self.session.commit()

	def delete_results(self, filters=None, commit=True):
		q = self.get_filtered_results_query(filters=filters)
		q.delete()
		if commit: self.session.commit()
	
	def get_filtered_results_query(self, filters=None):
		q = self.session.query(Result)
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
					(obj_class, obj_attr) = f['attr'].split('.')
					attr_code = "%s.%s" % (obj_class, obj_attr)
					join_code = "join(%s)" % obj_class
					value_code = "f['value']"

				# Handle all other attrs.
				else: 
					attr_code = "getattr(Effort, f['attr'])"
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
		sub_q = self.get_filtered_results_query(filters=filters).subquery()
		alias = aliased(Result, sub_q)

		# Get field values, grouped by cell, time and field.		
		value_sum = func.sum(alias.value).label('value_sum')
		q = self.session.query(alias.time, alias.field, Cell, value_sum)
		q = q.join(Cell)
		q = q.group_by(alias.time).group_by(alias.field).group_by(Cell)

		# Assemble results into c_t dictionary.
		for row in q.all():
			t_c_f.setdefault(row.time, {})
			t_c_f[row.time].setdefault(row.Cell, {})
			t_c_f[row.time][row.Cell][row.field] = row.value_sum

		return t_c_f

