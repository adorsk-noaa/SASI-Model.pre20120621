# @TODO: consider making something like a 'SweptAreaEffect' class to represent the objects
# we store as contact adjusted areas.  Seems to get used in several places...

class SASIModel:

	def __init__(self, t0=0, tf=10, dt=1, grid_model=None, effort_model=None, va=None, taus=None, omegas=None):
		
		# Start time.
		self.t0 = t0

		# End time.
		self.tf = tf

		# Timestep.
		self.dt = dt

		# Habitats
		self.grid_model = grid_model 
		
		# Fishing effort model.
		self.effort_model = effort_model

		# Vulnerability Assessment
		self.va = va

		# tau (stochastic modifier for recovery)
		if not taus:
			taus = {
					'0' : 1,
					'1' : 2,
					'2' : 5,
					'3' : 10
					}
		self.taus = taus

		# omega (stochastic modifier for damage)
		if not omegas:
			omegas = {
					'0' : 10,
					'1' : 25,
					'2' : 50,
					'3' : 100
					}
		self.omegas = omegas

		# Modified Swept Area.
		self.Z = []

		# Contact-Adjusted Swept Area
		self.A = [] 

		# Recovery.
		self.X = [] 

		# Adverse Effects.
		self.Y = [] 

		self.setup()

	def setup(self):

		# Get habitat types, grouped by gears that can be applied to those
		# habitat types. 
		self.h_by_g = self.va.get_habitats_by_gears()

		# Get feature codes, grouped by gears that can be applied to those
		# feature types.
		self.f_by_g = self.va.get_features_by_gears()
	
	def run(self):

		# Do setup stuff here for running? or in setup?

		# Iterate from t0 to tf...
		for t in range(self.t0, self.tf, self.dt):
			self.iterate(t)

	def iterate(self, t):

		# Initialize arrays for the timestep.
		for array in [self.Z, self.A, self.X, self.Y]:
			array.append({c.id: 0 for c in self.grid_model.get_cells()})
			

		# For each cell...
		for c in self.grid_model.get_cells():

			#
			# Contact-Adjusted Swept Areas
			# 

			# Initialize list of Contact-Adjusted Swept Areas
			# for the current timestep.
			# Swept Areas will be calculated at the level of individual
			# features, and will be stored as dictionaries with these keys:
			# (swept_area, habitat, gear, feature)
			self.A[t][c.id] = []

			# Get fishing efforts for the cell.
			cell_efforts = self.effort_model.get_effort(c, t)

			# For each effort...
			for effort in cell_efforts:

				# Get habitats which are relevant to the effort.
				relevant_habitats = []
				for habitat in c.habitats:
					habitat_type = (habitat.substrate.id, habitat.energy)
					if habitat_type in self.h_by_g[effort.gear]: relevant_habitats.append(habitat)

				# If there were relevant habitats...
				if relevant_habitats:
				
					# Distribute the effort's swept area equally over the habitats.
					swept_area_per_habitat = 1.0 * effort.swept_area/len(relevant_habitats)

					# For each habitat...
					for habitat in relevant_habitats:

						# Get the features for which the gear can be applied. 
						relevant_features = []
						for feature in habitat.features:
							if feature.id in self.f_by_g[effort.gear]: relevant_features.append(feature)

						# If there were relevant features...
						if relevant_features:

							# Get or initialize the list of feature efforts for this cell
							# for this timestep.
							feature_efforts = self.A[t][c.id]


							# Distribute the habitat's effort equally over the features.
							swept_area_per_feature= swept_area_per_habitat/len(relevant_features)
							
							# For each feature...
							for feature in relevant_features:

								# Add the resulting contact-adjusted
								# swept area to the cell.
								self.A[t][c.id].append(
										{
											'swept_area': swept_area_per_feature,
											'habitat': habitat,
											'gear': effort.gear,
											'feature': feature,
											}	
										)

		
			##
			## Adverse effects.
			##

			# Initialize list of adverse effects.
			# Adverse effects will be dictionaries with these keys:
			# (swept_area, habitat, gear, feature)
			self.Y[t][c.id] = []

			# For each contact-adjusted effort...
			for effort in self.A[t][c.id]:

				# Get susceptibility for the effort.
				susceptibility = self.va.get_susceptibility(
						gear_code = effort.get('gear'),
						substrate_code = effort.get('habitat').substrate.id,
						feature_code = effort.get('feature').id,
						energy = effort.get('habitat').energy
						)

				# Get stochastic modifier for the susceptibility
				omega = self.omegas.get(susceptibility)

				# Calculate adverse effect.
				adverse_effect_swept_area = effort.get('swept_area') * omega

				# Add resulting adverse effect to the cell.
				self.Y[t][c.id].append(
						{
							'swept_area': adverse_effect_swept_area,
							'habitat': effort.get('habitat'),
							'gear': effort.get('gear'),
							'feature': effort.get('feature')
							}
						)


			##
			## Recovery
			## 

			# Set recovery by summing recoveries from
			# previous damage.
			# Recoveries are stored as dictionaries.

			# Initialize list of recoveries.
			self.X[t][c.id] = []

			# For each previous timestep...
			for x_t in range(self.t0, t, self.dt):

				# For each adverse effect in the timestep...
				for effort in self.Y[x_t][c.id]:

					# Get recover for the effort.
					recovery = self.va.get_recovery(
							gear_code = effort.get('gear'),
							substrate_code = effort.get('habitat').substrate.id,
							feature_code = effort.get('feature').id,
							energy = effort.get('habitat').energy
							)

					# Get stochastic modifier for the susceptibility
					tau = self.taus.get(recovery)

					# If the time difference between 
					# when the damage occured (x_t) and the current timestep
					# time step is less than the habitat's
					# recovery time (tau), then the habitat is still
					# recovering, and we should add
					# to the habitat's recovery value.
					if (x_t - t) <= tau:

						# Calculate recovered area.
						# Recovered area per timestep is the effort's swept area
						# distribute equally over the reocvery period.
						recovered_area = effort.get('swept_area')/tau

						# Add resulting recovered area to the cell.
						self.X[t][c.id].append(
							{
								'recovered_area': recovered_area,
								'effort': effort
								}
							)

			# Set modified swept area for the timestep.
			#self.Z[t][c.id] = self.X[t][c.id] - self.Y[t][c.id]


