import sasi.conf.conf as conf
from sasi.va.va import VulnerabilityAssessment
from sasi.habitat.habitat_type import Habitat_Type
from sasi.habitat.substrate import Substrate
import sasi.util.va
import sasi.sa.session as sa_session
import sasi.sa.metadata as sa_metadata
import sasi.sa.habitat.habitat_type as sa_habitat_type


def main():
	# Read features from vulernability assessment.
	va_rows = sasi.util.va.read_va_from_csv(conf.conf['va_file'])
	va = VulnerabilityAssessment(rows = va_rows)	
	valid_habitat_types = va.get_habitat_types()

	# Get DB session.
	session = sa_session.get_session()
	
	# Clear habitat_types table.
	session.execute(sa_habitat_type.table.delete())
	session.commit()

	# For each valid habitat_type...
	for h in valid_habitat_types:

		# Get substrate object.
		substrate = session.query(Substrate).filter(Substrate.id == h[0]).one()

		# Create habitat_type object.
		habitat_type_obj = Habitat_Type(substrate=substrate, energy=h[1])

		# Add to session.
		session.add(habitat_type_obj)

	# Save to db. 
	session.commit()


if __name__ == '__main__': main()
