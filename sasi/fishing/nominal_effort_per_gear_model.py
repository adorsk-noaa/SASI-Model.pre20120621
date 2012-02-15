from sasi.fishing.effort_model import EffortModel
from sasi.fishing.effort import Effort

class NominalEffortPerGearModel(EffortModel):

	def __init__(self, grid_model=None, gears=None):
		self.grid_model = grid_model
		self.gears = gears

	def get_effort(self, cell_id=None, time=None):

		# Initialize a list of efforts.
		efforts = []

		# Get cell for the given location and time.
		cell = self.grid_model.get_cells(filters={'id': [cell_id]}).pop()

		# Set the nominal effort to be the cell's area.
		nominal_effort = cell.area

		# Get the list of gears.
		gears = self.gears
		
		# For each gear...
		for gear in gears:

			# Create an effort for the gear.
			efforts.append(Effort(gear=gear, swept_area=nominal_effort, location=cell_id, time=time))

		return efforts

