from sasi.dao.habitat.habitat_dao import Habitat_DAO
from sasi.habitat.habitat import Habitat
from sasi.util.habitat.habitat import generate_habitats


class Test_Habitat_DAO(Habitat_DAO):

	def __init__(self, num_habitats=10):
		self.habitats = {}

		num_cells = num_habitats/2

		n = 0
		for h in generate_habitats():
			self.habitats[h.id] = h
			n += 1		

	def get_habitats(self, filters=None):

		# By default, get all habitats.
		habitats = self.habitats.values()

		# Apply filters.
		if filters:
			for filter_name, filter_values in filters.items():
				habitats = [h for h in habitats if getattr(h,filter_name) in filter_values]

		return habitats
