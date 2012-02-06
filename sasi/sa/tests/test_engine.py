import unittest
import sasi.sa.engine as sa_engine

class EngineTest(unittest.TestCase):

	def test(self):
		e = sa_engine.get_engine()
		result = e.execute("select 1").scalar()
		self.failUnless(result)


if __name__ == '__main__':
	unittest.main()
