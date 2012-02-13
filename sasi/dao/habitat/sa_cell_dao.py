import sasi.sa.habitat.cell as sa_habitat
from sasi.dao.habitat.cell_dao import Cell_DAO
from sasi.habitat.cell import Cell


class SA_Cell_DAO(Cell_DAO):

	def __init__(self, session=None):
		self.session = session

	def get_cells(self, filters=None):
		q = self.session.query(Cell)

		if filters:
			for filter_name, filter_values in filters.items():
				q = q.filter(getattr(Cell, filter_name).in_(filter_values))

		return q.all()
