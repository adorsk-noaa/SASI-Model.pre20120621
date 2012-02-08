from sasi.fishing.effort_model import EffortModel
from sasi.fishing.effort import Effort

class NominalEffortModel(EffortModel):

	def __init__(self, effort_per_cell=1, grid_model=None, va=None):
		self.effort_per_cell = effort_per_cell
		self.grid_model = grid_model
		self.va = va

	def get_effort(self, cell=None, time=None):

		# Initialize a list of efforts.
		efforts = []

		nominal_effort = self.effort_per_cell

		# Get habitats for the given location and time.
		cell = self.grid_model.get_cells(filters={'type': ['id_km100'], 'id': [cell]})

		# For each habitat in the cell...
		for habitat in cell.habitats:

			# Set habitat's effort to be proportional to the area of the habitat.
			effort_per_habitat = nominal_effort * (habitat.area/cell.area)

			# Get gears for the given habitat
			gears = self.va.get_gears_by_habitats().get((habitat.substrate.id, habitat.energy)) 

			# If there were gears...
			if gears:

				# Set effort per gear to be proportional the number of gears.
				effort_per_gear = effort_per_habitat/len(gears)

				# Create an effort for each gear.
				efforts.extend([Effort(gear=g, swept_area=effort_per_gear, location=cell, time=time) for g in gears])

		return efforts

