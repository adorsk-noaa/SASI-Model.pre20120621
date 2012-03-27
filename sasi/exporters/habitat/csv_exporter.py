import exporter as habitat_exporter
from cStringIO import StringIO
import csv

class CsvExporter(habitat_exporter.Exporter):

	def __init__(self):
		habitat_exporter.Exporter.__init__(self)
	
	def export(self, habitats=[]):
		csv_buffer = StringIO()
		writer = csv.writer(csv_buffer)

		fields = [
				'id',
				'substrate_name',
				'substrate_id',
				'energy',
				'depth_meters',
				'area_meters2',
				'geom_wkt',
				]

		writer.writerow(fields)

		for h in habitats:
			writer.writerow([self.get_field(h,field) for field in fields])

		return csv_buffer.getvalue()

