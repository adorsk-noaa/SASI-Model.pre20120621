import sasi.conf.conf as conf
from sasi.va.va import VulnerabilityAssessment
from sasi.habitat.habitat_type import Habitat_Type
from sasi.habitat.feature import Feature
from sasi.habitat.substrate import Substrate
import sasi.util.va
import sasi.sa.session as sa_session
import sasi.sa.metadata as sa_metadata
import sasi.sa.habitat.habitat_type as sa_habitat_type


def main():
	# Read habitat types and features from vulnerability assessment.
	va_rows = sasi.util.va.read_va_from_csv(conf.conf['va_file'])
	va = VulnerabilityAssessment(rows = va_rows)	
	valid_habitat_types = va.get_habitats()
	features_by_habs = va.get_features_by_habitats()

	# Get DB session.
	session = sa_session.get_session()
	
	# Clear habitat_types table.
	session.execute(sa_habitat_type.habitat_type_feature_table.delete())
	session.execute(sa_habitat_type.habitat_type_table.delete())
	session.commit()

	# For each valid habitat_type...
	for h in valid_habitat_types:

		(substrate_id,energy) = h.split(',')

		# Get substrate object.
		substrate = session.query(Substrate).filter(Substrate.id == substrate_id).one()

		# Get features.
		features_for_hab = features_by_habs[h]
		features = []
		for category_features in features_for_hab.values():
			features.extend([session.query(Feature).filter(Feature.id == f).one() for f in category_features])

		# Create habitat_type object.
		habitat_type_obj = Habitat_Type(substrate=substrate, energy=energy, features=features)

		# Add to session.
		session.add(habitat_type_obj)

	# Save to db. 
	session.commit()


if __name__ == '__main__': main()
