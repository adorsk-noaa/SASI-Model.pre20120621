class Habitat:

	def __init__(self, **opts):
		self.substrate = opts.get("substrate", '')
		self.energy = ''
		self.features = []
		self.area = 0.0
		self.location = None

