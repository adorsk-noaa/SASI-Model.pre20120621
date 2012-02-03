import unittest
import sasi.sqlalchemy.session as sa_session

class SessionTest(unittest.TestCase):

	def test(self):
		session = sa_session.get_session()
		self.failUnless(session)


if __name__ == '__main__':
	unittest.main()
