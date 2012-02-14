import sasi.conf.conf as conf
from sasi.va.va import VulnerabilityAssessment
from sasi.habitat.habitat import Habitat
from sasi.habitat.substrate import Substrate
import sasi.util.va
import sasi.sa.session as sa_session
import sasi.sa.metadata as sa_metadata
import sasi.sa.habitat.habitat as sa_habitat


def main():
	# Read features from vulernability assessment.
	va_rows = sasi.util.va.read_va_from_csv(conf.conf['va_file'])
	va = VulnerabilityAssessment(rows = va_rows)	
	valid_habitats = va.get_habitats()

	# Get DB session.
	session = sa_session.get_session()
	
	# Clear habitats table.
	session.execute(sa_habitat.table.delete())
	session.commit()

	# For each valid habitat...
	for h in valid_habitats:

		# Get substrate object.
		substrate = session.query(Substrate).filter(Substrate.id == h[0]).one()

		# Create habitat object.
		habitat_obj = Habitat(substrate=substrate, energy=h[1])

		# Add to session.
		session.add(habitat_obj)

	# Save to db. 
	session.commit()


if __name__ == '__main__': main()
