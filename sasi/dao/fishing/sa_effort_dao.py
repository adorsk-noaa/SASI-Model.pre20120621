import sasi.sa.fishing.effort
import sasi.sa.fishing.effort_set
from sasi.habitat.cell import Cell
from sasi.fishing.effort import Effort
from sasi.fishing.effort_set import Effort_Set

from sqlalchemy import func
from sqlalchemy.orm import aliased

class SA_Effort_DAO(object):

	def __init__(self, session=None):
		self.session = session

	def get_efforts(self, filters=None):
		q = self.get_filtered_efforts_query(filters=filters)
		return q.all()

	def get_efforts_as_effort_set(self, effort_set_id=None, filters=None):
		q = self.get_filtered_efforts_query(filters=filters)
		return Effort_Set(
				id = effort_set_id,
				efforts = q.all()
				)

	def save_efforts(self, efforts, commit=True):
		self.session.add_all(efforts)
		if commit: self.session.commit()

	def delete_efforts(self, filters=None, commit=True):
		q = self.get_filtered_efforts_query(filters=filters)
		q.delete()
		if commit: self.session.commit()
	
	def get_effort_sets(self, filters=None):
		q = self.get_filtered_effort_sets_query(filters)
		return q.all()

	def delete_effort_sets(self, filters=None, commit=True):
		q = self.get_filtered_effort_sets_query(filters)
		q.delete()
		if commit: self.session.commit()

	def save_effort_sets(self, effort_sets=None, commit=True):
		for effort_set in effort_sets:
			self.session.add(effort_set)
		if commit: self.session.commit()
	
	def get_filtered_efforts_query(self, filters=None):
		q = self.session.query(Effort)
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

				# Handle effort_set_id.
				if f['attr'] == 'effort_set_id':
					attr_code = "Effort_Set.id"
					join_code = "join(Effort_Set.efforts)"
					value_code = f['value']

				# Handle effort_sets.
				elif f['attr'] == 'effort_sets':
					attr_code = "Effort_Set.id"
					join_code = "join(Effort_Set.efforts)"
					value_code = "[es.id for es in f['value']]"

				# Handle cells.
				elif f['attr'] == 'cells':
					attr_code = "Cell.id"
					join_code = "join(Cell)"
					value_code = "[c.id for c in f['value']]"

				# Handle all other attrs.
				else: 
					attr_code = "getattr(Effort, f['attr'])"
					value_code = f['value']

				# Assemble filter.
				filter_code = "q = q.filter(%s%s(%s))" % (attr_code, op_code, value_code)
				if join_code: filter_code += ".%s" % join_code

				
				# Compile and execute filter code to create filter.
				compiled_filter_code = compile(filter_code, '<query>', 'exec')
				exec compiled_filter_code

		# Return query.
		return q

	def get_filtered_effort_sets_query(self, filters=None):
		q = self.session.query(Effort_Set)
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

				# Handle effort_sets attr.
				if f['attr'] == 'effort_sets':
					attr_code = "Effort_Set.id"
					value_code = "[es.id for es in f['value']]"

				# Handle all other attrs.
				else: 
					attr_code = "getattr(Effort_Set, f['attr'])"
					value_code = f['value']

				# Assemble filter.
				filter_code = "q = q.filter(%s%s(%s))" % (attr_code, op_code, value_code)
				if join_code: filter_code += ".%s" % join_code

				# Compile and execute filter code to create filter.
				compiled_filter_code = compile(filter_code, '<query>', 'exec')
				exec compiled_filter_code
				
		# Return query.
		return q

