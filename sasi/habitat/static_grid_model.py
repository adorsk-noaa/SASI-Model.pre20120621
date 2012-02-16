from sasi.habitat.grid_model import GridModel

class StaticGridModel(GridModel):

	def __init__(self, cell_dao=None, default_filters=None):
		self.cell_dao = cell_dao
		self.default_filters = default_filters

	def get_cells(self, filters=None, override_default_filters=False):
		if self.default_filters and not filters:
			return self.cell_dao.get_cells(filters=self.default_filters)
		elif self.default_filters and filters and not override_default_filters:
			combined_filters = self.default_filters.copy()
			combined_filters.update(filters)
			return self.cell_dao.get_cells(filters=combined_filters)
		else:
			return self.cell_dao.get_cells(filters=filters)

