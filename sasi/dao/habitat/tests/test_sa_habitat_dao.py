import unittest
from sasi.sa.tests.basetest import BaseTest
from sasi.dao.habitat.sa_habitat_dao import SA_Habitat_DAO
import sasi.sa.habitat.habitat_metadata as sa_habitat_metadata

class SA_Habitat_DAOTest(BaseTest):

	def test(self):
		habitat_dao = SA_Habitat_DAO(session=self.session)

		hab_id_filter = {'attr': 'Habitat.id', 'op': 'in', 'value': [2]}
		feature_id_filter = {'attr': 'Habitat_Type.Feature.id', 'op': '==', 'value': 'B06'}
		substrate_id_filter = {'attr': 'Habitat_Type.Substrate.id', 'op': '==', 'value': 'S1'}
		energy_filter = {'attr': 'Habitat_Type.energy', 'op': '==', 'value': 'Low'}

		filters = [
				hab_id_filter,
				feature_id_filter,
				substrate_id_filter,
				energy_filter
				]

		#habitats = habitat_dao.get_habitats()
		#print habitats
		connection_str = habitat_dao.get_mapserver_connection_string()
		#print connection_str
		data_str = habitat_dao.get_mapserver_data_string(filters=filters)
		#print data_str
		substrates = habitat_dao.get_substrates_for_habitats(filters=filters)
		#print substrates
		energies = habitat_dao.get_energys_for_habitats(filters=filters)
		#print energies
		habitat_types = habitat_dao.get_habitat_types_for_habitats(filters=filters)
		#print habitat_types

		features = habitat_dao.get_features_for_habitats(filters = filters)
		#print features

		fields = [
				"Habitat.area"
				]
		grouping_fields = [
				"Habitat_Type.Substrate.id"
				]
		filters = [
				#energy_filter
				hab_id_filter
				]
		habitat_dao.get_stats(fields=fields, grouping_fields=grouping_fields, filters=filters)

	def get_session(self):
		return self.session

if __name__ == '__main__':
	unittest.main()
