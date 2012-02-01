import unittest
import sasi.sqlalchemy.engine as sa_engine

class EngineTest(unittest.TestCase):

	def test(self):
		e = sa_engine.engine
		result = e.execute("select 1").scalar()
		self.failUnless(result)


if __name__ == '__main__':
	unittest.main()
