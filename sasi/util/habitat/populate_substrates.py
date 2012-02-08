import sasi.conf.conf as conf
from sasi.va.va import VulnerabilityAssessment
from sasi.habitat.substrate import Substrate
import sasi.util.va
import sasi.sa.habitat.substrate as sa_substrate
import sasi.sa.session as sa_session

def main():
	# Read substrates from vulernability assessment.
	va_rows = sasi.util.va.read_va_from_csv(conf.conf['va_file'])
	va = VulnerabilityAssessment(rows = va_rows)	
	f_by_h = va.get_features_by_habitats()
	substrates = va.get_substrates()

	# Get DB session.
	session = sa_session.get_session()
	
	# Clear substrate table.
	session.execute(sa_substrate.table.delete())
	session.commit()

	# Create Substrate objects
	# note: might move this into the VA object itself later.
	substrate_objs = []
	for s in substrates.values():
		s_obj = Substrate(name=s['SUBSTRATE'], id=s['SUBSTRATE_CODE'])
		substrate_objs.append(s_obj)

	# Add substrate objects to session and save to DB.
	session.add_all(substrate_objs)
	session.commit()


if __name__ == '__main__': main()
