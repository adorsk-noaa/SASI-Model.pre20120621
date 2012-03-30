import unittest
import sasi.exporters.habitat.shp_exporter as shp_exporter
import sasi.util.habitat.habitat as habitat_util

class ShpTest(unittest.TestCase):

	def test(self):
		exporter = shp_exporter.ShpExporter()

		habitats = habitat_util.generate_habitats(n=10, geom_wkb=True)

		export = exporter.export(habitats)
		#print export

		self.failUnless(True)


if __name__ == '__main__':
	unittest.main()




