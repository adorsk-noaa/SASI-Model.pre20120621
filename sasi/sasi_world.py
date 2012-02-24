import sasi.sa.session as sa_session
from sasi.dao.habitat.test_cell_dao import Test_Cell_DAO
from sasi.dao.habitat.sa_cell_dao import SA_Cell_DAO
from sasi.dao.habitat.sa_feature_dao import SA_Feature_DAO
from sasi.dao.va.csv_va_dao import CSV_VA_DAO
from sasi.dao.results.sa_result_dao import SA_Result_DAO
from sasi.dao.fishing.sa_effort_dao import SA_Effort_DAO
from sasi.fishing.nominal_effort_per_gear_model import NominalEffortPerGearModel
from sasi.fishing.dao_effort_model import DAO_Effort_Model
from sasi.fishing.gear import Gear

from sasi.sasi_model import SASIModel

import sasi.conf.conf as conf

from sasi.habitat.static_grid_model import StaticGridModel
from sasi.habitat.features_model import Features_Model

from sasi.results.result_set import Result_Set

from datetime import datetime
import sys

import sasi.util.sasi_model as sasi_model_util


if __name__ == '__main__':

	conf.conf['verbose'] = True

	db_session = sa_session.get_session()

	#if conf.conf['verbose']: db_session.bind.echo = True

	result_dao = SA_Result_DAO(session=db_session)

	effort_dao = SA_Effort_DAO(session=db_session)

	t0 = 1989	
	tf = 2010
	dt = 1
	times = range(t0,tf+1,dt)

	# Get or create persistent result set to hold results.
	# Will overwrite an existing set of the same name.
	#result_set_id = 'realized_gc30'
	result_set_id = 'tmp' 
	result_set = None
	fetched_sets = result_dao.get_result_sets(filters=[{'attr': 'id', 'op': 'in', 'value': [result_set_id]}])
	if not fetched_sets:
		result_set = Result_Set(id=result_set_id)
	else: 
		result_set = fetched_sets[0]
	result_set.results = []

	#grid_model = StaticGridModel(cell_dao=Test_Cell_DAO(), default_filters={'type': 'km100'}) 
	grid_model = StaticGridModel(cell_dao=SA_Cell_DAO(session=db_session), default_filters=[{'attr': 'type','value': ['km100'] }, {'attr': 'type_id', 'value': ['817']}]) 
	#grid_model = StaticGridModel(cell_dao=SA_Cell_DAO(session=db_session), default_filters=[{'attr': 'type','value': ['km100'] }]) 

	# Filter domain for cells w/ depth less than 138 (for G3).
	#grid_model = StaticGridModel(cell_dao=SA_Cell_DAO(session=db_session), default_filters=[{'attr': 'type','value': ['km100'] }, {'attr': 'depth', 'op': '>=', 'value': -138}]) 

	va_dao = CSV_VA_DAO()
	va = va_dao.load_va()

	features_model = Features_Model(feature_dao=SA_Feature_DAO(session=db_session))

	gears = []
	#for i in range(1,6+1):
	for i in [3]:
		gear_code = "GC%s" % i
		gears.append(db_session.query(Gear).filter(Gear.id == gear_code).one())


	#effort_model = NominalEffortPerGearModel(grid_model=grid_model, gears=gears, times=times)
	effort_model = DAO_Effort_Model(effort_dao = effort_dao, default_filters=[
		{
			'attr': 'effort_set_id',
			'op': '==',
			'value': "legacy_realized_a"
			},
		{
			'attr': 'Gear.id',
			'op': '==',
			'value': 'GC30'
			},

		{
			'attr': 'Cell.type_id',
			'op': '==',
			'value': '817'
			}
		])

	taus = {
			'0': 1,
			'1': 2,
			'2': 4,
			'3': 8 
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

	for n in times:
		print >> sys.stderr, "iteration: %s" % n
		print >> sys.stderr, datetime.now()
		model.iterate(n)
	
	# Print results as csv.
	sasi_model_util.results_to_csv_buffer(results=model.results, buffer=sys.stdout)

	# Add raw results to results collection.
	#tmp_result_set = sasi_model_util.results_to_result_set(
			#results = model.results 
			#)
	#result_set.results.extend(tmp_result_set.results)

	# Save the collection.
	#result_dao.save_result_sets(result_sets=[result_set])
