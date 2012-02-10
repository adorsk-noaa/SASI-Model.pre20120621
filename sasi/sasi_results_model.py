from shove import Shove

class SASI_Results_Model(object):

	def __init__(self, basename="results"):

		for result_type in ['A', 'Y', 'X', 'Z']:
			setattr(self.__class__, result_type, Shove("sqlite:///%s.%s.sqlite" % (basename, result_type)))
