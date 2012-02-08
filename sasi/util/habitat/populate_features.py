import sasi.conf.conf as conf
from sasi.va.va import VulnerabilityAssessment
from sasi.habitat.feature import Feature
import sasi.util.va
import sasi.sa.habitat.feature as sa_feature
import sasi.sa.session as sa_session

def main():
	# Read features from vulernability assessment.
	va_rows = sasi.util.va.read_va_from_csv(conf.conf['va_file'])
	va = VulnerabilityAssessment(rows = va_rows)	
	features = va.get_features()

	# Get DB session.
	session = sa_session.get_session()
	
	# Clear features table.
	session.execute(sa_feature.table.delete())
	session.commit()

	# Create Feature objects
	# note: might move this into the VA object itself later.
	feature_objs = []
	for f in features.values():
		f_obj = Feature(name=f['FEATURE'], id=f['FEATURE_CODE'], category=f['FEATURE_CLASS_CODE'])
		feature_objs.append(f_obj)

	# Add feature objects to session and save to DB.
	session.add_all(feature_objs)
	session.commit()


if __name__ == '__main__': main()
