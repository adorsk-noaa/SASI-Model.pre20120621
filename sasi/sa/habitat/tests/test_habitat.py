import unittest
from sasi.sa.tests.basetest import BaseTest
import sasi.sa.habitat.habitat as sa_habitat
import sasi.sa.habitat.feature as sa_feature
import sasi.sa.habitat.substrate as sa_substrate
import sasi.sa.habitat.cell as sa_cell
import sasi.habitat.tests.test_habitat as test_habitat
import sasi.habitat.tests.test_substrate as test_substrate
import sasi.habitat.tests.test_feature as test_feature
import sasi.util.habitat.habitat as habitat_util

from sqlalchemy import MetaData
from geoalchemy import *
from geoalchemy.geometry import Geometry

class HabitatTest(BaseTest):

	def test(self):
		s = self.session

		# Combine tables into one metadata
		# in order to resolve dependencies.
		combined_metadata = MetaData()
		for m in [sa_habitat, sa_feature, sa_substrate, sa_cell]:
			for t in m.metadata.tables.values():
				new_t = t.tometadata(combined_metadata)

				# Run DDL if table has geometry columns.
				has_geom = False
				for c in new_t.columns:
					if isinstance(c.type, Geometry): has_geom = True
				if has_geom: GeometryDDL(new_t)

		# Drop/Create tables.
		combined_metadata.drop_all(s.bind)
		combined_metadata.create_all(s.bind)

		# Generate test habitats
		substrate = test_substrate.generate_substrates(1).pop()
		s.add(substrate)
		
		features = test_feature.generate_features(1)
		s.add_all(features)

		h = habitat_util.generate_habitats(1).pop()
		h.substrate = substrate
		h.features = features

		# Add to the session and commit.
		s.add(h)
		s.commit()

		self.failUnless(True)

if __name__ == '__main__':
	unittest.main()
	
