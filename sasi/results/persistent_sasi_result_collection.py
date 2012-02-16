from sasi.results.sasi_result_collection import SASI_Result_Collection

class Persistent_SASI_Result_Collection(SASI_Result_Collection):

	def __init__(self, dao = None, id = id, results = None):
		self.dao = dao
		self.id = id

		# Try to load existing collection.
		collection = self.load()
		if collection:
			self.collection = collection
		# If there was no existing collection then create a new one.
		else:
			self.collection = SASI_Result_Collection(id = self.id, results=results)
		
		# Results is pointer to collection results.
		self.results = self.collection.results

	def get_results(self, filters=None):
		return self.dao.get_collection_results(self.collection, filters=filters)

	def delete_results(self, results=None, filters=None):
		self.dao.delete_collection_results(self.collection, results=results, filters=filters)

	def add_results(self, results):
		self.results.extend(results)

	def load(self):
		load_result = self.dao.get_collections(filters={'id': [self.id]})
		if load_result: return load_result.pop()
		else: return None

	def save(self):
		self.dao.save_collection(self.collection)
	
	def delete(self):
		self.dao.delete_collections(collections=[self.collection])
		


