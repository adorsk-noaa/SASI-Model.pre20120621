from sasi.habitat.grid_model import GridModel

class StaticGridModel(GridModel):

	def __init__(self, cell_dao=None):
		self.cell_dao = cell_dao

	def get_cells(self, filters=None):
		return self.cell_dao.get_cells(filters=filters)

