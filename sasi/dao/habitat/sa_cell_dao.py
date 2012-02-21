import sasi.sa.habitat.cell as sa_habitat
from sasi.dao.habitat.cell_dao import Cell_DAO
from sasi.habitat.cell import Cell
from sqlalchemy import func


class SA_Cell_DAO(Cell_DAO):

	def __init__(self, session=None):
		self.session = session

	def get_cells(self, filters=None):
		q = self.session.query(Cell)
		if filters:
			for f in filters:
				
				# Default operator is 'in'.
				if not f.has_key('op'): f['op'] = 'in'


				if f['op'] == 'in':
					q = q.filter(getattr(Cell, f['attr']).in_(f['value']))

				# Dynamically set filter operator.
				else:
					code = compile("q = q.filter(getattr(Cell, f['attr']) %s f['value'])" % f['op'], '<query>', 'exec')
					exec code

		return q.all()
