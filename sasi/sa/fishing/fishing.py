import sasi.sa.session as sa_session
import sasi.sa.metadata as sa_metadata
import sasi.sa.fishing.gear as sa_gear
import sasi.sa.fishing.effort as sa_effort
import sasi.sa.fishing.effort_set as sa_effort_set

def create_schema():
	
	session = sa_session.get_session()

	tables = [
			sa_gear.table,
			sa_effort.table,
			sa_effort_set.effort_set_table,
			sa_effort_set.effort_set_effort_table
			]

	for t in tables:
		t.create(session.bind)


