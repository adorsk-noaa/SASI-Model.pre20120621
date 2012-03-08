import unittest
import sasi.viz.habitat.map.mapserver as habitat_ms

class Habitat_Mapserver_Test(unittest.TestCase):

	def test(self):
		habitat_ms.get_map_image_from_wms(parameters=None, habitat_dao=None)
		self.failUnless(True)


if __name__ == '__main__':
	unittest.main()




