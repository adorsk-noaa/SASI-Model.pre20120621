import sys

def main():

	# Populating modules,  in run order.
	populating_modules = [
			'populate_substrates',
			'populate_features',
			'populate_habitat_types',
			'populate_habitats',
			'populate_cells',
			]

	for m in populating_modules:
		m_name = "sasi.util.habitat.%s" % m
		__import__(m_name)
		imported_m = sys.modules[m_name]
		imported_m.main()
	

if __name__ == '__main__': main()
