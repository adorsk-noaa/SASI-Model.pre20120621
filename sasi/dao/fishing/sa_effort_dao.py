import sasi.sa.fishing.effort
from sasi.habitat.cell import Cell
from sasi.fishing.gear import Gear
from sasi.fishing.effort import Effort

from sqlalchemy import func
from sqlalchemy.orm import aliased

class SA_Effort_DAO(object):

	def __init__(self, session=None):
		self.session = session

	def get_efforts(self, filters=None):
		q = self.get_filtered_efforts_query(filters=filters)
		return q.all()

	def save_efforts(self, efforts, commit=True):
		self.session.add_all(efforts)
		if commit: self.session.commit()

	def delete_efforts(self, filters=None, commit=True):
		q = self.get_filtered_efforts_query(filters=filters)
		q.delete()
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

				# Handle gears.
				if f['attr'] == 'gears':
					attr_code = "Gear.id"
					join_code = "join(Gear)"
					value_code = "[g.id for g in f['value']]"

				# Handle attrs on related objects.
				elif '.' in f['attr']:
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

