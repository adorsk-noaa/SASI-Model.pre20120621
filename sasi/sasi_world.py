from sasi.dao.habitat.test_cell_dao import Test_Cell_DAO
from sasi.dao.va.csv_va_dao import CSV_VA_DAO
from sasi.fishing.nominal_effort_per_gear_model import NominalEffortPerGearModel
from sasi.fishing.gear import Gear

from sasi.sasi_results_model import SASI_Results_Model

from sasi.sasi_model import SASIModel


from sasi.habitat.static_grid_model import StaticGridModel

if __name__ == '__main__':

	grid_model = StaticGridModel(cell_dao=Test_Cell_DAO(), default_filters={'type': 'km100'}) 

	va_dao = CSV_VA_DAO()
	va = va_dao.load_va()

	gears = []
	for i in range(1,6+1):
		gear_code = "GC%s" % i
		gear = Gear(
				id=gear_code,
				name=gear_code
				)
		gears.append(gear)

	effort_model = NominalEffortPerGearModel(grid_model=grid_model, gears=gears)

	results_model = SASI_Results_Model()

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
			results_model=results_model,
			taus=taus,
			omegas=omegas
			)

	for n in range(t0, tf):
		print "iteration: %s" % n
		model.iterate(n)
		sample_size = 5
		for table_name in ['A', 'Y', 'X', 'Z']:
			table = getattr(model, table_name)
			print "table '%s': %s" % (table_name, [table[n].values()[0:5]] )



