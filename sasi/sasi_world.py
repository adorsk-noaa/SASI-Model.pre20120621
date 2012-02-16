import sasi.sa.session as sa_session
from sasi.dao.habitat.test_cell_dao import Test_Cell_DAO
from sasi.dao.habitat.sa_cell_dao import SA_Cell_DAO
from sasi.dao.habitat.sa_feature_dao import SA_Feature_DAO
from sasi.dao.va.csv_va_dao import CSV_VA_DAO
from sasi.fishing.nominal_effort_per_gear_model import NominalEffortPerGearModel
from sasi.fishing.gear import Gear

from sasi.sasi_model import SASIModel

import sasi.conf.conf as conf

from sasi.habitat.static_grid_model import StaticGridModel
from sasi.habitat.features_model import Features_Model

from datetime import datetime
import sys

import sasi.util.sasi_model as sasi_model_util


if __name__ == '__main__':

	conf.conf['verbose'] = True

	db_session = sa_session.get_session()
	
	#grid_model = StaticGridModel(cell_dao=Test_Cell_DAO(), default_filters={'type': 'km100'}) 
	grid_model = StaticGridModel(cell_dao=SA_Cell_DAO(session=db_session), default_filters={'type': ['km100'], 'type_id': ['0']}) 
	#grid_model = StaticGridModel(cell_dao=SA_Cell_DAO(session=db_session), default_filters={'type': ['km100']}) 

	va_dao = CSV_VA_DAO()
	va = va_dao.load_va()

	features_model = Features_Model(feature_dao=SA_Feature_DAO(session=db_session))

	gears = []
	#for i in range(1,6+1):
	for i in [3]:
		gear_code = "GC%s" % i
		gear = Gear(
				id=gear_code,
				name=gear_code
				)
		gears.append(gear)

	effort_model = NominalEffortPerGearModel(grid_model=grid_model, gears=gears)

	t0 = 1
	tf = 6
	dt = 1
	taus = {
			'0': 1,
			'1': 1,
			'2': 2,
			'3': 4 
			}

	omegas = {
			'0': 0.05,
			'1': .175,
			'2': .375,
			'3': .75
			}
	
	model = SASIModel(
			t0=t0,
			tf=tf,
			dt=dt,
			grid_model=grid_model,
			features_model=features_model,
			effort_model=effort_model,
			va=va,
			taus=taus,
			omegas=omegas
			)

	for n in range(t0, tf+1):
		print >> sys.stderr, "iteration: %s" % n
		print >> sys.stderr, datetime.now()
		model.iterate(n)
	
	# Print results as csv.
	#sasi_model_util.results_to_csv_buffer(results=model.results, buffer=sys.stdout)

	# Get SASI Result Collection from results.
	result_collection = sasi_model_util.results_to_sasi_results_collection('myresults', results=model.results)
