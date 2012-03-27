import unittest
import sasi.exporters.habitat.csv_exporter as csv_exporter
import sasi.util.habitat.habitat as habitat_util

class CsvTest(unittest.TestCase):

	def test(self):
		exporter = csv_exporter.CsvExporter()

		habitats = habitat_util.generate_habitats(n=10)

		csv_export = exporter.export(habitats)
		print csv_export

		self.failUnless(True)


if __name__ == '__main__':
	unittest.main()




