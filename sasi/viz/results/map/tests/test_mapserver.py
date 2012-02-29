import unittest
import sasi.conf.conf as conf
import sasi.viz.results.map.mapserver as results_mapserver

class Results_Mapserver_Test(unittest.TestCase):

	def test(self):
		results_mapserver.get_results_map()
		self.failUnless(True)


if __name__ == '__main__':
	unittest.main()




