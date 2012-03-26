import unittest
from sasi.sa.tests.basetest import BaseTest
from sasi.dao.habitat.sa_habitat_dao import SA_Habitat_DAO
import sasi.sa.habitat.habitat_metadata as sa_habitat_metadata

class SA_Habitat_DAOTest(BaseTest):

	def test(self):
		habitat_dao = SA_Habitat_DAO(session=self.session)

		hab_id_filter = {'field': 'id', 'op': 'in', 'value': [2]}
		feature_id_filter = {'field': 'habitat_type.features.id', 'op': '==', 'value': 'B06'}
		substrate_id_filter = {'field': 'habitat_type.substrate.id', 'op': '==', 'value': 'S1'}
		energy_filter = {'field': 'habitat_type.energy', 'op': '==', 'value': 'Low'}

		filters = [
				hab_id_filter,
				#feature_id_filter,
				#substrate_id_filter,
				#energy_filter
				]

		#habitats = habitat_dao.get_habitats()
		#print habitats
		connection_str = habitat_dao.get_mapserver_connection_string()
		#print connection_str
		data_str = habitat_dao.get_mapserver_data_string(filters=filters)
		#print data_str

		fields = [
				{'id': "area", 'label': 'area_label'}
				]
		grouping_fields = [
				{'id': "habitat_type.substrate.id", 'label': 'substrate_id'}
				]
		filters = [
				#energy_filter
				#hab_id_filter
				]
		aggregates = habitat_dao.get_aggregates(fields=fields, grouping_fields=grouping_fields, filters=filters)
		#for a in aggregates: print a.keys(), a

		histogram = habitat_dao.get_histogram(bucket_field={'id': 'z', 'label': 'depth', 'transform': "-1 * {field}"}, filters=filters)
		#for b in histogram: print b


	def get_session(self):
		return self.session

if __name__ == '__main__':
	unittest.main()
