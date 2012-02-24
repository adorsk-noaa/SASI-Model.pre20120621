import unittest
import sasi.conf.conf as conf
from sasi.va.va import VulnerabilityAssessment
import sasi.util.va

class VulnerabilityAssessmentTest(unittest.TestCase):

	def test(self):
		va_rows = sasi.util.va.read_va_from_csv(conf.conf['va_file'])
		va = VulnerabilityAssessment(rows = va_rows)	
		f_by_h = va.get_features_by_habitats()
		features = va.get_features()
		substrates = va.get_substrates()
		g_by_h = va.get_gear_categories_by_habitats()
		gear_categories = va.get_gear_categories()
		h_by_g = va.get_habitats_by_gear_categories()
		habitats_for_gear = va.get_habitats_for_gear_category(gear_categories.keys().pop())
		features_for_gear = va.get_features_for_gear_category(gear_categories.keys().pop())
		f_by_g = va.get_features_by_gear_categories()
		habitats = va.get_habitats()

if __name__ == '__main__':
	unittest.main()
