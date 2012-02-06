from sasi.dao.habitat.sa_habitatdao import SA_HabitatDAO

class SASIWorld(object):

	def __init__(self, habitats_dao=None):
		self.habitats_dao = habitats_dao
		self.habitats = self.setup_habitats()
	
	# Get habitats from persistence layer.
	def setup_habitats(self):
		habitats = self.habitats_dao.load_habitats()
		return habitats

if __name__ == '__main__':

	habitats_dao = SA_HabitatDAO()

	sasi_world = SASIWorld(habitats_dao=habitats_dao)


