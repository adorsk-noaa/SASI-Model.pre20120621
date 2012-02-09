from sasi.fishing.effort_model import EffortModel
from sasi.fishing.effort import Effort

class NominalEffortModel(EffortModel):

	def __init__(self, grid_model=None, va=None):
		self.grid_model = grid_model
		self.va = va

	def get_effort(self, cell=None, time=None):

		# Initialize a list of efforts.
		efforts = []

		# Get cell for the given location and time.
		cell = self.grid_model.get_cells(filters={'type': ['km100'], 'id': [cell.id]}).pop()

		# Set the nominal effort to be the cell's area.
		nominal_effort = cell.area

		# Get the list of gears.
		gears = self.va.get_gears()

		# Get habitat types, grouped by gears that can be applied to those
		# habitat types. 
		h_by_g = self.va.get_habitats_by_gears()

		# Get feature codes, grouped by gears that can be applied to those
		# feature types.
		f_by_g = self.va.get_features_by_gears()
		
		# For each gear...
		for gear_code in gears.keys():
			
			# Get habitats in which the gear can be applied.
			relevant_habitats = []
			habitat_types_for_gear = h_by_g[gear_code]
			for habitat in cell.habitats:
				habitat_type = (habitat.substrate.id, habitat.energy)
				if habitat_type in habitat_types_for_gear: relevant_habitats.append(habitat)

			# If there were relevant habitats...
			if relevant_habitats:
				
				# Distribute the nominal effort equally over the habitats.
				effort_per_habitat = 1.0 * nominal_effort/len(relevant_habitats)

				# For each habitat...
				for habitat in relevant_habitats:

					# Get the features for which the gear can be applied. 
					relevant_features = []
					for feature in habitat.features:
						if feature.id in f_by_g[gear_code]: relevant_features.append(feature)

					# If there were relevant features...
					if relevant_features:

						# Distribute the habitat's effort equally over the features.
						effort_per_feature= effort_per_habitat/len(relevant_features)

						# Create an effort for the feature.
						efforts.append(Effort(gear=gear_code, swept_area=effort_per_feature, location=cell, time=time))

		return efforts

