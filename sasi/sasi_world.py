from sasi.dao.habitat.test_habitat_dao import Test_Habitat_DAO
from sasi.dao.va.csv_va_dao import CSV_VA_DAO

from sasi.sasi_model import SASIModel

class SASIWorld(object):

	def __init__(self, habitats_dao=None, va_dao=None):
		self.habitats_dao = habitats_dao
		self.va_dao = va_dao

		self.habitats = self.setup_habitats()
		
		self.va = self.setup_va()
	
	# Get habitats from persistence layer.
	def setup_habitats(self):
		habitats = self.habitats_dao.load_habitats()
		return habitats

	def setup_va(self)
		va = self.va_dao.load_va()
		return va

if __name__ == '__main__':

	habitats_dao = Test_HabitatDAO()

	va_dao = CSV_VA_DAO()

	sasi_world = SASIWorld(
			habitats_dao=habitats_dao
			va_da=va_dao
			)


	t0 = 0
	tf = 10
	dt = 1
	habitats = sasi_world.habitats
	va = sasi_world.va
	taus = {}
	omegas = {}
	
	model = SASIModel(
			t0=t0,
			tf=tf,
			dt=dt,
			habitats=habitats,
			va=va,
			taus=taus,
			omegas=omegas
			)

	for n in range(t0, tf):
		print "iteration: %s" % n

		model.iterate(n)



