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
			taus = {}
		self.taus = taus

		# omega (stochastic modifier for damage)
		if not omegas:
			omegas = {}
		self.omegas = omegas

		# Modified Swept Area.
		self.Z = []

		# Fishing effort.
		self.A = [] 

		# Recovery.
		self.X = [] 

		# Damage.
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
			# Effort
			# 

			# Initialize list of efforts for the current timestep.
			# Efforts will be stored as tuples in this form:
			# (habitat.id, gear.id, feature.id, swept_area)
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

								# Add the effort to the cell's efforts for the timestep.
								self.A[t][c.id].append(
										(
											swept_area_per_feature,
											habitat.id,
											effort.gear,
											feature.id,
											)
										)

			
			# Initialize list of damages.
			self.Y[t][c.id] = []

			# For each effort...
			for e in self.A[t][c.id]:

				# For each of the habitat's features...

				# Get VA for effort.
				#effort_va = self.va.assessments((e.gear, h.substrate.id, h

				# Set damage for each effort.
				# Damage is stored as (effort, damage) pairs.
				damage = 1
				#self.Y[t][c.id] = self.A[t][c.id] * self.omegas.get(h,1)
				#self.Y[t][c.id] = self.A[t][c.id] * self.omegas.get(h,1)

			# Set recovery by summing recoveries from
			# previous damage.
			# For each previous timestep...
			for x_t in range(self.t0, t, self.dt):

				# If the time difference between 
				# when the damage occured (x_t) and the current timestep
				# time step is less than the habitat's
				# recovery time (tau), then the habitat is still
				# recovering, and we should add
				# to the habitat's recovery value.
				if (x_t - t) <= self.taus.get(c.id,1):

					# We recover a proportion of the previous damagei
					# based on the habitat's recovery time.
					#self.X[t][c.id] = self.A[x_t][c.id]/self.taus.get(h,1)
					pass 

			# Set modified swept area for the timestep.
			#self.Z[t][c.id] = self.X[t][c.id] - self.Y[t][c.id]


