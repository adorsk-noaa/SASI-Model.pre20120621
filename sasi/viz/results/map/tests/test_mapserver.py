import unittest
import sasi.conf.conf as conf
import sasi.viz.results.map.mapserver as results_ms
from sasi.dao.results.sa_result_dao import SA_Result_DAO
from sasi.sa.tests.basetest import BaseTest

class Results_Mapserver_Test(BaseTest):

	def test(self):
		s = self.session
		result_dao = SA_Result_DAO(session=s)

		# Generate WMS request parameters.
		wms_parameters = {
				'SERVICE': 'WMS' ,
				'VERSION': '1.1.0', 
				'REQUEST': 'GetMap', 
				'LAYERS': 'data',
				'SRS':'EPSG:4326',
				#'BBOX':'-180.0,-90.0,180.0,90.0',
				'BBOX': '-80,31,-65,45',
				'FORMAT':'image/gif',
				'WIDTH':'640',
				'HEIGHT':'640',
				}
		
		result_field = {
				'field': 'Y',
				'min': 47563742,
				#'min': 0,
				#'max': 70235000
				'min': .0,
				'max': 1
				}

		base_filters = [
				{'field': 'time', 'op': '==', 'value': '2009'},
				{'field': 'tag', 'op': '==', 'value': 'gc30_all'}
				]
		filters = []
		img = results_ms.get_map_image_from_wms(wms_parameters=wms_parameters.items(), result_field=result_field, result_dao=result_dao, filters=base_filters + filters)
		print img

		self.failUnless(True)


if __name__ == '__main__':
	unittest.main()




