import sasi.conf.conf as conf

from sasi.results.sasi_results_model import SASI_Results_Model

def main():
	results = SASI_Results_Model()

	#print results.A
	print len(results.A[0])

if __name__ == '__main__': main()
