import unittest
from sasi.sa.tests.basetest import BaseTest
import sasi.sa.habitat.habitat as sa_habitat
import sasi.sa.habitat.feature as sa_feature
import sasi.sa.habitat.substrate as sa_substrate
import sasi.habitat.tests.test_habitat as test_habitat
import sasi.habitat.tests.test_substrate as test_substrate
import sasi.habitat.tests.test_feature as test_feature

class HabitatTest(BaseTest):

	def test(self):
		s = self.session

		# Initialize tables (order matters for dependencies).
		tables = [
				sa_habitat.habitats_features_table,
				sa_habitat.table,
				sa_feature.table,
				sa_substrate.table,
				]

		for t in tables:
			if t.exists(s.bind): t.drop(s.bind)

		for t in reversed(tables):
			t.create(s.bind)

		# Generate test habitats
		substrate = test_substrate.generate_substrates(1).pop()
		s.add(substrate)
		
		features = test_feature.generate_features(1)
		s.add_all(features)

		h = test_habitat.generate_habitats(1).pop()
		h.substrate = substrate
		h.features = features

		# Add to the session and commit.
		s.add(h)
		s.commit()

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()
	
