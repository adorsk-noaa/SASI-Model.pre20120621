class SASI_Result_Collection(object):

	def __init__(self, id = id, results = None):
		self.id = id
		self.results = results
	
	def add_results(self, results):
		self.results.extend(results)


