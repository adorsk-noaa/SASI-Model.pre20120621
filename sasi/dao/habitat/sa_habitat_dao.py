import sasi.sa.session as sa_session
import sasi.sa.habitat.habitat as sa_habitat
from sasi.dao.habitat.habitat_dao import Habitat_DAO
from sasi.habitat.habitat import Habitat


class SA_Habitat_DAO(Habitat_DAO):

	def __init__(self): pass

	def get_session(self):
		return sa_session.get_session()

	def load_habitats(self, ids=None):
		session = self.get_session()

		habitats = []

		# If ids were given, filter by ids.
		if ids:
			habitats = session.query(Habitat).filter(Habitat.id.in_(ids)).all()

		# Otherwise load all habitats
		else:
			habitats = session.query(Habitat).all()

		return habitats
