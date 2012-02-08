import sasi.sa.session as sa_session
import sasi.sa.habitat.cell as sa_habitat
from sasi.dao.habitat.cell_dao import Cell_DAO
from sasi.habitat.cell import Cell


class SA_Cell_DAO(Cell_DAO):

	def __init__(self): pass

	def get_session(self):
		return sa_session.get_session()

	def get_cells(self, filters=None):
		session = self.get_session()

		q = session.query(Cell)

		if filters:
			for filter_name, filter_values in filters.items():
				q = q.filter(getattr(Cell, filter_name).in_(filter_values))


		# Return query results
		return q.all()
