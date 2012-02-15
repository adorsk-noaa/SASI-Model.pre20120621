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
		imported_m = __import__("sasi.util.habitat.%s" % m)
		print m
		#imported_m.main()
	

if __name__ == '__main__': main()
