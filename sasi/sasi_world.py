from sasi.dao.habitat.test_habitat_dao import Test_Habitat_DAO
from sasi.dao.va.csv_va_dao import CSV_VA_DAO
from sasi.fishing.nominal_effort_model import NominalEffortModel

from sasi.sasi_model import SASIModel

from sasi.habitat.static_grid_habitat_model import StaticGridHabitatModel

if __name__ == '__main__':

	habitat_model = StaticGridHabitatModel(habitat_dao=Test_Habitat_DAO()) 

	va_dao = CSV_VA_DAO()
	va = va_dao.load_va()

	effort_model = NominalEffortModel(habitat_model=habitat_model, va=va)

	t0 = 0
	tf = 10
	dt = 1
	taus = {}
	omegas = {}
	
	model = SASIModel(
			t0=t0,
			tf=tf,
			dt=dt,
			habitat_model=habitat_model,
			effort_model=effort_model,
			va=va,
			taus=taus,
			omegas=omegas
			)

	for n in range(t0, tf):
		print "iteration: %s" % n

		model.iterate(n)



