class Result_Set(object):

	def __init__(self, id = id, results = []):
		self.id = id
		self.results = results
	
	def add_results(self, results):
		self.results.extend(results)


