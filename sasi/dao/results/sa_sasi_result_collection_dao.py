import sasi.sa.results.sasi_result_collection as sa_sasi_result_collection
import sasi.sa.results.sasi_result as sa_sasi_result
from sasi.dao.results.sasi_result_collection_dao import SASI_Result_Collection_DAO
from sasi.results.sasi_result_collection import SASI_Result_Collection
from sasi.results.sasi_result import SASI_Result

class SA_SASI_Result_Collection_DAO(object):

	def __init__(self, session=None):
		self.session = session

	def get_collections(self, filters=None):
		q = self.session.query(SASI_Result_Collection)
		if filters:
			for filter_name, filter_values in filters.items():
				q = q.filter(getattr(SASI_Result_Collection, filter_name).in_(filter_values))

		return q.all()

	def add_collections(self, collections = None):
		for c in collections:
			self.session.add(c)
		self.session.commit()

	def delete_collections(self, collections = None, filters=None):
		if collections:
			for c in collections:
				self.session.merge(c)
				self.session.delete(c)

		elif filters:
			for c in self.get_collections(filters=filters):
				self.session.delete(c)
		
		self.session.commit()

	def get_collection_results(self, collection, filters=None):
		q = self.session.query(SASI_Result).join(SASI_Result_Collection).filter(SASI_Result_Collection.id == collection.id)
		if filters:
			for filter_name, filter_values in filters.items():
				q = q.filter(getattr(SASI_Result, filter_name).in_(filter_values))

		return q.all()

	def save_collection(self, collection):
		self.session.merge(collection)
		self.session.commit()
	
	def delete_collection_results(self, collection, results=None, filters=None):

		if results:
			for r in results: self.session.delete(r)

		elif filters:
			for r in self.get_collection_results(collection, filters=filters):
				self.session.delete(r)

		self.session.commit()
