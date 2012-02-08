class SASIModel:

	def __init__(self, t0=0, tf=10, dt=1, habitat_model=None, effort_model=None, va=None, taus={}, omegas={}):
		
		# Start time.
		self.t0 = t0

		# End time.
		self.tf = tf

		# Timestep.
		self.dt = dt

		# Habitats
		self.habitat_model = habitat_model 
		
		# Fishing effort model.
		self.effort_model = effort_model

		# Vulnerability Assessment
		self.va = va

		# tau (stochastic modifier for recovery)
		self.taus = taus

		# omega (stochastic modifier for damage)
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

		# Shortcut to gears by habitat lookup.
		self.g_by_h = self.va.get_gears_by_habitats()
	
	def run(self):

		# Do setup stuff here for running? or in setup?

		# Iterate from t0 to tf...
		for t in range(self.t0, self.tf, self.dt):
			self.iterate(t)

	def iterate(self, t):

		# Initialize arrays for the timestep.
		for array in [self.Z, self.A, self.X, self.Y]:
			array.append({h.id: 0 for h in self.habitat_model.get_habitats()})
			

		# For each habitat...
		for h in self.habitat_model.get_habitats():
		
			# Initialize list of efforts for the current timestep.
			self.A[t][h.id] = []

			# Get fishing efforts for the habitat's cell.
			cell_efforts = self.effort_model.get_effort(h.id_km100, t)

			# Keep fishing efforts which apply to the habitat,
			# and distribute efforts evenly over features.
			habitat_efforts = []
			habitat_gears = self.g_by_h.get((h.substrate.id, h.energy),[])
			for e in cell_efforts:
				if e.gear in habitat_gears:
					self.A[t][h.id].append(e)
			
			
			# Initialize list of damages.
			self.Y[t][h.id] = []

			# For each effort...
			for e in self.A[t][h.id]:

				# For each of the habitat's features...

				# Get VA for effort.
				effort_va = self.va.assessments((e.gear, h.substrate.id, h

				# Set damage for each effort.
				# Damage is stored as (effort, damage) pairs.
				damage = 
				self.Y[t][h.id] = self.A[t][h.id] * self.omegas.get(h,1)

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
				if (x_t - t) <= self.taus.get(h.id,1):

					# We recover a proportion of the previous damagei
					# based on the habitat's recovery time.
					self.X[t][h.id] = self.A[x_t][h.id]/self.taus.get(h,1)

			# Set modified swept area for the timestep.
			self.Z[t][h.id] = self.X[t][h.id] - self.Y[t][h.id]


