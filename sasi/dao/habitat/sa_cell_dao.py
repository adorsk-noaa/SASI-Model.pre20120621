import sasi.sa.habitat.cell as sa_habitat
from sasi.dao.habitat.cell_dao import Cell_DAO
from sasi.dao.sa_dao import SA_DAO
from sasi.habitat.cell import Cell
from sqlalchemy import func


class SA_Cell_DAO(Cell_DAO, SA_DAO):

	def __init__(self, session=None):

		# Create class registry for SA_DAO parent class.
		class_registry = {}
		for clazz in [Cell]:
			class_registry[clazz.__name__] = clazz

		SA_DAO.__init__(self, session, primary_class=Cell, class_registry=class_registry)

	def get_cells(self, filters=None):
		q = self.get_filtered_query(filters=filters)
		return q.all()
