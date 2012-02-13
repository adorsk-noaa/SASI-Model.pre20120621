from shove import Shove

import sasi.conf.conf as conf

class SASI_Results_Model(object):

	def __init__(self, basename="//" + conf.conf['output_dir'] + "/results"):

		for result_type in ['A', 'Y', 'X', 'Z']:
			setattr(self.__class__, result_type, Shove("sqlite://%s.%s.sqlite" % (basename, result_type)))
