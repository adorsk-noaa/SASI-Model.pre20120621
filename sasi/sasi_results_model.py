class SASI_Results_Model(object):

	def __init__(self, results_dao=None):
		self.results_dao = results_dao

	def get_results(self, filters=None):
		return self.results_dao.get_results(filters=filters)

	def create_result(self, result):
		self.results_dao.create_results(results=[result])

	def update_result(self, result):
		self.results_dao.update_results(results=[result])

	def create_or_update_result(self, result):
		results = self.get_results(
				filters=[
					{
						'name': 'results',
						'operator': '==',
						'values': [result]
						}
					]
				)

		if results:
			self.update_result(result)
		else:
			self.create_result(result)

		

		
