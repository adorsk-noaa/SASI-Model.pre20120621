class Habitat(object):

	def __init__(self, id_km100=None, id_km1000=None, id_vor=None, z=None, substrate=None, energy=None, features=[], area=None, geom=None, id=None):
		self.id = id
		self.id_km100 = id_km100
		self.id_km1000 = id_km1000
		self.id_vor = id_vor
		self.z = z
		self.substrate = substrate
		self.energy = energy
		self.features = features
		self.area = area
		self.geom = geom

