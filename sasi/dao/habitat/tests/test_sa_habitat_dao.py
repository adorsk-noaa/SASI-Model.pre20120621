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
		feature_id_filter2 = {'field': 'habitat_type.features.id', 'op': 'in', 'value': ['B02','B03']}

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
				#{'id': "habitat_type.substrate.id", 'label': 'substrate_id', 'label_field': {'id': 'habitat_type.substrate.name'}, 'all_values': True},
				#{'id': "habitat_type.energy", 'label': 'energy', 'all_values': True},
				#{'id': "habitat_type.features.id", 'label': 'feature_id', 'label_field': {'id': 'habitat_type.features.name'}, 'all_values': True},
				{'id': "z", 'label': 'depth', 'as_histogram': True, 'all_values': True, 'min': 0, 'max': 3000, 'transform': '-1 * {field}'},
				]
		filters = [
				substrate_id_filter
				#energy_filter
				#hab_id_filter
				]
		print "here"
		aggregates = habitat_dao.get_aggregates(fields=fields, grouping_fields=grouping_fields, filters=filters)
		data = []
		import re
		for c in aggregates['children'].values():
			label = c['label']
			value = c['data'][0]['value']
			m = re.match('(.*) to (.*)', label)
			if m:
				cmin = float(m.group(1))
			data.append({
				'label': label,
				'value': value,
				'min': cmin
				})
		import operator
		data = sorted(data, key=operator.itemgetter('min'))
		for d in data:
			print "{}:\t{:.1e}".format(d['label'], d['value'])


	def get_session(self):
		return self.session

if __name__ == '__main__':
	unittest.main()
