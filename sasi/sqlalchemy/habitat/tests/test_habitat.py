import unittest
from sasi.sqlalchemy.tests.basetest import BaseTest
import sasi.sqlalchemy.habitat.habitat as sa_habitat
import sasi.sqlalchemy.habitat.feature as sa_feature
import sasi.sqlalchemy.habitat.substrate as sa_substrate
import sasi.habitat.tests.test_habitat as test_habitat
import sasi.habitat.tests.test_substrate as test_substrate
import sasi.habitat.tests.test_feature as test_feature

class HabitatTest(BaseTest):

	def test(self):
		s = self.session

		# Initialize tables
		for m in [sa_feature, sa_substrate, sa_habitat]:
			m.metadata.drop_all(s.bind)
			m.metadata.create_all(s.bind)

		# Generate test habitats
		substrate = test_substrate.generate_substrates(1).pop()
		s.add(substrate)
		
		feature = test_feature.generate_features(1).pop()
		s.add(feature)

		h = test_habitat.generate_habitats(1).pop()
		h.substrate = substrate
		h.features = feature

		# Add to the session and commit.
		s.add(h)
		s.commit()

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()
	
