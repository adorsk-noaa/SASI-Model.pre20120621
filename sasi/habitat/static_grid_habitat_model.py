from sasi.habitat.habitat_model import HabitatModel

class StaticGridHabitatModel(HabitatModel):

	def __init__(self, habitat_dao=None):
		self.habitat_dao = habitat_dao

	def get_habitats(self, cell=None, time=None):
		return self.habitat_dao.get_habitats(filters={'id_km100': [cell]})

