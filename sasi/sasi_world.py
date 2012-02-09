from sasi.dao.habitat.test_cell_dao import Test_Cell_DAO
from sasi.dao.va.csv_va_dao import CSV_VA_DAO
from sasi.fishing.nominal_effort_model import NominalEffortModel

from sasi.sasi_model import SASIModel

from sasi.habitat.static_grid_model import StaticGridModel

if __name__ == '__main__':

	grid_model = StaticGridModel(cell_dao=Test_Cell_DAO()) 

	va_dao = CSV_VA_DAO()
	va = va_dao.load_va()

	effort_model = NominalEffortModel(grid_model=grid_model, va=va)

	t0 = 0
	tf = 10
	dt = 1
	taus = {}
	omegas = {}
	
	model = SASIModel(
			t0=t0,
			tf=tf,
			dt=dt,
			grid_model=grid_model,
			effort_model=effort_model,
			va=va,
			taus=taus,
			omegas=omegas
			)

	for n in range(t0, tf):
		print "iteration: %s" % n

		model.iterate(n)


