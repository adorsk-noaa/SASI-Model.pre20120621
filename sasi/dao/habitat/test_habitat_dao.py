from sasi.dao.habitat.habitat_dao import Habitat_DAO
from sasi.habitat.habitat import Habitat
from sasi.util.habitat.habitat import generate_habitats


class Test_Habitat_DAO(Habitat_DAO):

	def __init__(self, num_habitats=10): 
		self.habitats = {}

		for h in generate_habitats(num_habitats):
			self.habitats[h.id] = h


	def load_habitats(self, ids=None):
		habitats = []

		# If ids were given, filter by ids.
		if ids:
			habitats = [self.habitats[id] for id in ids if id in self.habitats.keys()]

		# Otherwise load all habitats
		else:
			habitats = self.habitats.values()

		return habitats
