from sasi.dao.habitat.cell_dao import Cell_DAO
from sasi.habitat.cell import Cell
import sasi.util.habitat.habitat as habitat_util


class Test_Cell_DAO(Cell_DAO):

	def __init__(self, num_cells=10):
		self.cells = {}

		n = 0
		for c in habitat_util.generate_cells(num_cells, default_area = lambda: (1000.0 * 100)**2 ):
			c.id = n
			c.type='km100'
			self.cells[n] = c
			n += 1		

	def get_cells(self, filters=None):

		# By default, get all habitats.
		cells = self.cells.values()

		# Apply filters.
		if filters:
			for f in filters:
				code = compile("cells = [c for c in cells if getattr(c, f['attr']) %s f['value'] ]" % f['op'], '<code>', 'exec')
				exec code

		return cells
