import unittest
import sasi.conf
from sasi.va.va import VulnerabilityAssessment
import sasi.util.va

class VulnerabilityAssessmentTest(unittest.TestCase):

	def test(self):
		va_rows = sasi.util.va.read_va_from_csv(sasi.conf.conf['va_file'])
		va = VulnerabilityAssessment(rows = va_rows)	
		f_by_h = va.get_features_by_habitats()
		features = va.get_features()
		print features
if __name__ == '__main__':
	unittest.main()
