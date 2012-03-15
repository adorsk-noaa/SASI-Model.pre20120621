from sasi.dao.sa_dao import SA_DAO
import sasi.sa.fishing.effort
from sasi.habitat.cell import Cell
from sasi.fishing.gear import Gear
from sasi.fishing.effort import Effort

from sqlalchemy import func
from sqlalchemy.orm import aliased

class SA_Effort_DAO(SA_DAO):

	def __init__(self, session=None):

		# Create class registry for SA_DAO parent class.
		class_registry = {}
		for clazz in [Cell, Gear, Effort]:
			class_registry[clazz.__name__] = clazz

		SA_DAO.__init__(self, session, primary_class=Effort, class_registry=class_registry)

	def get_efforts(self, filters=None):
		q = self.get_filtered_query(filters=filters)
		return q.all()

	def save_efforts(self, efforts, commit=True):
		self.session.add_all(efforts)
		if commit: self.session.commit()

	def delete_efforts(self, filters=None, commit=True):
		q = self.get_filtered_query(filters=filters)
		q.delete()
		if commit: self.session.commit()
	

