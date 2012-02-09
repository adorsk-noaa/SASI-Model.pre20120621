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
		self.Z = {} 

		# Contact-Adjusted Swept Area
		self.A = {} 

		# Recovery.
		self.X = {} 

		# Adverse Effects.
		self.Y = {} 

		# List of index keys to be used when creating index results.
		self.index_keys = self.get_index_keys()

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

		# Initialize tables for the timestep if not already initialized.
		for table in [self.Z, self.A, self.X, self.Y]:
			table.setdefault(t, self.get_indexed_table())

		# For each cell...
		for c in self.grid_model.get_cells():

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

							# Distribute the habitat's effort equally over the features.
							swept_area_per_feature= swept_area_per_habitat/len(relevant_features)

							# For each feature...
							for feature in relevant_features:

								# Generate an index key for the results.
								index_key = self.get_index_key(
										cell_id = c.id,
										substrate_code = habitat.substrate.id,
										energy = habitat.energy,
										gear_code = effort.gear,
										feature_code = feature.id
										)

								# Calculate contact-adjusted swept area.
								contact_adjusted_swept_area = swept_area_per_feature

								# Add the resulting contact-adjusted
								# swept area to the A table.
								self.A[t][index_key] += contact_adjusted_swept_area

								# Get vulnerability assessment for the effort.
								vulnerability_assessment = self.va.get_assessment(
									gear_code = effort.gear,
									substrate_code = habitat.substrate.id,
									feature_code = feature.id,
									energy = habitat.energy
									)

								# Get stochastic modifiers 
								omega = self.omegas.get(vulnerability_assessment['S'])
								tau = self.taus.get(vulnerability_assessment['R'])

								# Calculate adverse effect swept area.
								adverse_effect_swept_area = contact_adjusted_swept_area * omega

								# Add to adverse effect table.
								self.Y[t][index_key] += adverse_effect_swept_area

								# Calculate recovery per timestep.
								recovery_per_dt = adverse_effect_swept_area/tau

								# Add recover to future recovery table entries.
								for future_t in (t + 1, t + tau, self.dt):
									self.X.setdefault(future_t, self.get_indexed_table())
									self.X[future_t][index_key] += recovery_per_dt

								# Add to modified swept area for the timestep.
								self.Z[t][index_key] += self.X[t][index_key] - self.Y[t][index_key]


	# Get index keys for storing model effects. 
	# The keys consist of valid (cell, substrate, energy, gear, feature) combinations,
	# as defined by the grid model and the vulnerability assessment.
	def get_index_keys(self):
		index_keys = [] 
		for c in self.grid_model.get_cells():
			for a in self.va.assessments.values():
				index_key = self.get_index_key(cell_id = c.id,
						substrate_code = a['SUBSTRATE_CODE'],
						energy = a['ENERGY'],
						gear_code = a['GEAR_CODE'],
						feature_code = a['FEATURE_CODE']
					)	
				index_keys.append(index_key)
		return index_keys

	# Format index key from key components.
	def get_index_key(self, cell_id='', substrate_code='', energy='', gear_code='', feature_code=''):
		index_key = (
				cell_id,	
				substrate_code,
				energy,
				gear_code,
				feature_code
				)
		return index_key

	# Get a storage table indexed by the index keys.
	# note: at some later point this might need optimization later, e.g. w/ pytables
	def get_indexed_table(self):
		table = {}
		for k in self.index_keys:
			table[k] = 0.0
		return table
		

		






