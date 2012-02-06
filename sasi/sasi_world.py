from sasi.dao.habitat.test_habitatdao import Test_HabitatDAO
from sasi.sasi_model import SASIModel

class SASIWorld(object):

	def __init__(self, habitats_dao=None):
		self.habitats_dao = habitats_dao
		self.habitats = self.setup_habitats()
	
	# Get habitats from persistence layer.
	def setup_habitats(self):
		habitats = self.habitats_dao.load_habitats()
		return habitats

if __name__ == '__main__':

	habitats_dao = Test_HabitatDAO()

	sasi_world = SASIWorld(habitats_dao=habitats_dao)

	t0 = 0
	tf = 10
	dt = 1
	habitats = sasi_world.habitats
	taus = {}
	omegas = {}
	
	model = SASIModel(
			t0=t0,
			tf=tf,
			dt=dt,
			habitats=habitats,
			taus=taus,
			omegas=omegas
			)

	for n in range(t0, tf):
		print "iteration: %s" % n

		model.iterate(n)



