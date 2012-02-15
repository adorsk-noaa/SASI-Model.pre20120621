from sasi.dao.habitat.habitat_dao import Habitat_DAO
from sasi.habitat.habitat import Habitat
import sasi.util.habitat.habitat as habitat_util


class Test_Habitat_DAO(Habitat_DAO):

	def __init__(self, num_habitats=10):
		self.habitats = {}

		for h in habitat_util.generate_habitats(num_habitats):
			self.habitats[h.id] = h

	def get_habitats(self, filters=None):

		# By default, get all habitats.
		habitats = self.habitats.values()

		# Apply filters.
		if filters:
			for filter_name, filter_values in filters.items():
				habitats = [h for h in habitats if getattr(h,filter_name) in filter_values]

		return habitats
