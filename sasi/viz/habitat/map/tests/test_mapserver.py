import unittest
import sasi.viz.habitat.map.mapserver as habitat_ms
from sasi.dao.habitat.sa_habitat_dao import SA_Habitat_DAO
from sasi.sa.tests.basetest import BaseTest

class Habitat_Mapserver_Test(BaseTest):

	def test(self):
		s = self.session
		habitat_dao = SA_Habitat_DAO(session=s)

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
				'HEIGHT':'640'
				}
		
		img = habitat_ms.get_map_image_from_wms(wms_parameters=wms_parameters.items(), habitat_dao=habitat_dao)
		#print img

		self.failUnless(True)


if __name__ == '__main__':
	unittest.main()




