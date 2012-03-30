import exporter as habitat_exporter
import csv

class CsvExporter(habitat_exporter.Exporter):

	def __init__(self):
		habitat_exporter.Exporter.__init__(self)
	
	def export(self, habitats=[]):

		# Make tmpdir to hold export.
		tmp_dir = self.mkdtemp()

		csv_file_h = open("{}/habitats.csv".format(tmp_dir), "w")
		writer = csv.writer(csv_file_h)

		fields = [
				'id',
				'substrate_name',
				'substrate_id',
				'energy',
				'features',
				'depth_meters',
				'area_meters2',
				'geom_wkt',
				]

		writer.writerow(fields)

		for h in habitats:
			writer.writerow([self.get_field(h,field) for field in fields])

		csv_file_h.close()

		# Package the export.
		package_file = self.make_package(export_dir=tmp_dir)

		return package_file

