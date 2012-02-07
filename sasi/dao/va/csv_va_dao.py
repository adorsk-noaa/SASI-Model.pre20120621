from sasi.dao.va.va_dao import VA_DAO
import sasi.util.va
import sasi.conf.conf as conf
from sasi.va.va import VulnerabilityAssessment

class CSV_VA_DAO(VA_DAO):

	def __init__(self):
		pass

	def load_va(self): 
		va_rows = sasi.util.va.read_va_from_csv(conf.conf['va_file'])
		va = VulnerabilityAssessment(rows = va_rows)	
		return va


		
