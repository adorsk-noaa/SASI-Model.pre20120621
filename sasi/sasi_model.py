# @TODO: consider making something like a 'SweptAreaEffect' class to represent the objects
# we store as contact adjusted areas.  Seems to get used in several places...

import sasi.conf.conf as conf
import sys

class SASIModel:

	def __init__(self, t0=0, tf=10, dt=1, grid_model=None, features_model=None, effort_model=None, va=None, taus=None, omegas=None):
		
		# Start time.
		self.t0 = t0

		# End time.
		self.tf = tf

		# Timestep.
		self.dt = dt

		# Grid
		self.grid_model = grid_model 

		# Features.
		self.features_model = features_model 
		
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

		# Results.
		self.results = {}
		for field in [
				'A', # Contact-Adjusted Swept Area.
				'X', # Recovered Swept Area.
				'Y', # Modified Swept Area.
				'Z', # Instantaneous X - Y
				'ZZ', # Cumulative Z.
				]:
			self.results[field] = {}

		self.setup()

	def setup(self):
		# Get habitat types, grouped by gears that can be applied to those
		# habitat types. 
		self.h_by_g = self.va.get_habitats_by_gears()

		# Get feature codes, grouped by gears that can be applied to those
		# feature types.
		self.f_by_g = self.va.get_features_by_gears()

		# Get features grouped by category, keyed by habitat types.
		self.f_by_h = self.va.get_features_by_habitats()

		# Create cells-habitat_type-feature lookup to improve perfomance.
		# Assumes static habitats.
		self.c_ht_f = self.get_c_ht_f_lookup()
	
	def get_c_ht_f_lookup(self):

		# Initialize cell-habitat_type-feature lookup.
		c_ht_f = {}

		# For each cell...
		for c in self.grid_model.get_cells():

			# Create entry in c_ht_f for cell.
			c_ht_f[c] = {
					'ht': {}
					}

			# Get cell's habitats.
			cell_habitats = c.habitats

			# Group habitats by habitat type.
			habitats_by_type = {}
			for h in cell_habitats:
				habitat_type = h.habitat_type
				habitats_by_type.setdefault(habitat_type, [])
				habitats_by_type[habitat_type].append(h)

			# For each habitat type...
			for ht in habitats_by_type.keys():

				# Create entry for ht in c_ht_f.
				c_ht_f[c]['ht'][ht] = {}

				# Calculate combined area.
				ht_area = sum([h.area for h in habitats_by_type[ht]])
				c_ht_f[c]['ht'][ht]['area'] = ht_area

				# Calculate percentage of cell area.
				c_ht_f[c]['ht'][ht]['percent_cell_area'] = ht_area/c.area

				# Get features for habitat, grouped by featured category.
				c_ht_f[c]['ht'][ht]['f'] = {}
				for feature_category, feature_ids in self.f_by_h[ht.id].items():
					features = self.features_model.get_features(filters={'id': feature_ids})
					c_ht_f[c]['ht'][ht]['f'][feature_category] = features 

		return c_ht_f
		
	
	def run(self):

		# Iterate from t0 to tf...
		for t in range(self.t0, self.tf + 1, self.dt):
			self.iterate(t)

	def iterate(self, t):

		# For each cell...
		cell_counter = 0
		for c in self.c_ht_f.keys():

			if conf.conf['verbose']:
				if (cell_counter % 100) == 0: print >> sys.stderr, "\tc: %s" % cell_counter

			cell_counter += 1

			# Get contact-adjusted fishing efforts for the cell.
			cell_efforts = self.effort_model.get_effort(c, t)

			# For each effort...
			for effort in cell_efforts:

				# Get cell's habitat types which are relevant to the effort.
				relevant_habitat_types = []
				for ht in self.c_ht_f[c]['ht'].keys():
					if ht.id in self.h_by_g[effort.gear.id]: relevant_habitat_types.append(ht)

				# If there were relevant habitat types...
				if relevant_habitat_types:

					# Calculate the total area of the relevant habitats.
					relevant_habitats_area = sum([self.c_ht_f[c]['ht'][ht]['area'] for ht in relevant_habitat_types])

					# For each habitat type...
					for ht in relevant_habitat_types:
					
						# Distribute the effort's swept area proportionally to the habitat type's area as a fraction of the total relevant area.
						swept_area_per_habitat_type = effort.swept_area * (self.c_ht_f[c]['ht'][ht]['area']/relevant_habitats_area)

						# Get feature categories.
						# @TODO: get categories from config or VA.
						feature_categories = ['2']

						# Distribute swept area equally across feature categories.
						# @TODO: maybe weight this? rather than just num categories?
						#swept_area_per_feature_category = swept_area_per_habitat/len(feature_categories)
						swept_area_per_feature_category = swept_area_per_habitat_type/2

						# For each feature category...
						for fc in feature_categories:

							# Get the features for which the gear can be applied. 
							relevant_features = []
							for f in self.c_ht_f[c]['ht'][ht]['f'].get(fc,[]):
								if f.id in self.f_by_g[effort.gear.id]: relevant_features.append(f)

							# If there were relevant features...
							if relevant_features:

								# Distribute the category's effort equally over the features.
								swept_area_per_feature = swept_area_per_feature_category/len(relevant_features)

								# For each feature...
								for f in relevant_features:

									# Generate an index key for the results.
									index_key = self.get_index_key(
											time = t,
											cell = c,
											habitat_type = ht,
											gear = effort.gear,
											feature = f
											)

									# Add the resulting contact-adjusted
									# swept area to the A table.
									self.results['A'][index_key] = self.results['A'].get(index_key,0.0) + swept_area_per_feature

									# Get vulnerability assessment for the effort.
									vulnerability_assessment = self.va.get_assessment(
										gear_code = effort.gear.id,
										habitat_key = ht.id,
										feature_code = f.id,
										)

									# Get stochastic modifiers 
									omega = self.omegas.get(vulnerability_assessment['S'])
									tau = self.taus.get(vulnerability_assessment['R'])

									# Calculate adverse effect swept area.
									adverse_effect_swept_area = swept_area_per_feature * omega

									# Add to adverse effect table.
									self.results['Y'][index_key] = self.results['Y'].get(index_key,0.0) + adverse_effect_swept_area

									# Calculate recovery per timestep.
									recovery_per_dt = adverse_effect_swept_area/tau

									# Add recover to future recovery table entries.
									for future_t in range(t + 1, t + tau + 1, self.dt):
										if future_t <= self.tf:
											future_key = self.get_index_key(
													time = future_t,
													cell = c,
													habitat_type = ht,
													gear = effort.gear,
													feature = f
													)
											self.results['X'][future_key] = self.results['X'].get(future_key, 0.0) + recovery_per_dt 

									# Add to modified swept area for the timestep.
									self.results['Z'][index_key] = self.results['Z'].get(index_key, 0.0) + self.results['X'].get(index_key, 0.0) - self.results['Y'][index_key]

									# Add to cumulative (assumes previous timesteps have been run).
									if t > self.t0:
										past_key = self.get_index_key(
												time = t - self.dt,
												cell = c,
												habitat_type = ht,
												gear = effort.gear,
												feature = f
												)
										self.results['ZZ'][index_key] = self.results['ZZ'].get(index_key, 0.0) + self.results['ZZ'][past_key] + self.results['Z'][index_key]
									else:
										self.results['ZZ'][index_key] = self.results['ZZ'].get(index_key, 0.0) + self.results['Z'][index_key]


	# Format index key from key components.
	def get_index_key(self, time=None, cell=None, habitat_type=None, gear=None, feature=None):
		index_key = (
				time,
				cell,	
				habitat_type,
				gear,
				feature
				)

		return index_key
