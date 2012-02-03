import unittest
from sqlalchemy.orm import sessionmaker
import sasi.sqlalchemy.engine as sa_engine

class BaseTest(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.engine = sa_engine.get_engine()
		print cls.engine
		cls.Session = sessionmaker()

	def setUp(self):
		connection = self.engine.connect()

		# begin a non-ORM transaction
		self.trans = connection.begin()

		# bind an individual Session to the connection
		#Session.configure(bind=connection)
		self.session = self.Session(bind=connection)
		#Entity.session = self.session

	def tearDown(self):
		# rollback - everything that happened with the
		# Session above (including calls to commit())
		# is rolled back.
		self.trans.rollback()
		self.session.close()
