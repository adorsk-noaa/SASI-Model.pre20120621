class SASIModel:

	def __init__(self):
		
		# Start time.
		self.t0 = 0

		# End time.
		self.tf = 0

		# Timestep.
		self.dt = 1

		# Modified Swept Area.
		self.Z = [] 

		# Fishing effort.
		self.A = [] 

		# Recovery.
		self.X = [] 

		# Damage.
		self.Y = [] 

		# Habitats
		self.habitats = []

		# tau (stochastic modifier for recovery)
		self.tau = {}

		# omega (stochastic modifier for damage)
		self.omega = {}

	def setup(self): pass
	
	def run(self):

		# Do setup stuff here for running? or in setup?

		# Iterate from t0 to tf...
		for t in range(self.t0, self.tf, self.dt):
			self.iterate(t)

	def iterate(self, t):

		# Initialize arrays for the timestep.
		for array in [self.Z, self.A, self.X, self.Y]:
			array.append([0] * len(self.habitats))
			

		for h in self.habitats:
			
			# Set fishing effort area.
			# @todo: ADD LOGIC TO GET EFFORT FROM MODEL OR EXTERNAL DATA
			self.A[t][h] = 1

			# Set damage.
			self.Y[t][h] = 1

			# Set recovery by summing recoveries from
			# previous damage for the current timestep.
			# For each previous timestep...
			for x_t in range(self.t0, t, self.dt):

				# If the time difference between 
				# when the damage occured (x_t) and the current timestep
				# time step is less than the habitat's
				# recovery time (tau), then the habitat is still
				# recovering, and we should add
				# to the habitat's recovery value.
				if (x_t - t) <= self.tau.get(h):

					# We recover a proportion of the previous damagei
					# based on the habitat's recovery time.
					self.X[t][h] = self.A[x_t][h]/h.tau

			# Set modified swept area for the timestep.
			self.Z[t][h] = self.X[t][h] - self.Y[t][h]


