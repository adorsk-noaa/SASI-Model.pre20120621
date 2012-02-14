class Habitat(object):

	def __init__(self, id=None, substrate=None, energy=None):
		self.substrate = substrate
		self.energy = energy
		self.id = "%s,%s" % (self.substrate.id,self.energy)

