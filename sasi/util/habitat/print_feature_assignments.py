import sasi.conf.conf as conf
from sasi.va.va import VulnerabilityAssessment
import sasi.util.va

import pprint

def main():

	pp = pprint.PrettyPrinter(indent=4)

	# Read features from vulernability assessment.
	va_rows = sasi.util.va.read_va_from_csv(conf.conf['va_file'])
	va = VulnerabilityAssessment(rows = va_rows)	

	# Get features by habitat.
	f_by_h = va.get_features_by_habitats()

	# Combine geo and bio features into one list for each habitat.
	combined_f_by_h = {}
	for h, features in f_by_h.items():
		combined_features = list(features['1'].union(features['2']))
		combined_f_by_h[h] = combined_features
	
	print "assignments = %s" % pp.pformat(combined_f_by_h)

	
if __name__ == '__main__': main()
