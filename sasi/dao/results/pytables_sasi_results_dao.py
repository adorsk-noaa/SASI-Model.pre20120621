from sasi.dao.results.results_dao import Results_DAO
import tables as pytables

# Class to represent an individual SASI result row.
class SASI_Result(pytables.IsDescription):
	key = pytables.StringCol(128)
	result_type = pytables.StringCol(8)
	time = pytables.IntCol()
	substrate = pytables.StringCol(8)
	energy = pytables.StringCol(8)
	gear = pytables.StringCol(8)
	value = pytables.Float32Col()

class Pytables_SASI_Results_DAO(Results_DAO):

	def __init__(self, h5file_path=None): 

		# Path to h5file.
		self.h5file_path = h5file_path

		# Handle to h5file (to be opened in setup() )
		self.h5file = None

		# Results table.
		self.results_table = None

		# Result components to use for uniquely identifying results.
		self.key_components = ['result_type', 'time', 'substrate', 'energy', 'gear']

		self.setup()
		
	def setup(self):
		
		# Open hd5 file in write mode.
		self.h5file = pytables.openFile(self.h5file_path, mode = "w", title = "SASI Results Group")

		# Create a new group under '/'
		group = self.h5file.createGroup('/', 'results', 'Results Group')

		# Create SASI result table.
		self.results_table = self.h5file.createTable(group, 'results', SASI_Result, 'SASI Results Table')

	# Generate a key string for this result.
	def get_key_for_result(self, result):
		return ','.join(["%s" % result.get(kc,'') for kc in self.key_components])


	def get_results(self, filters=None, as_proxy=False):
	
		if filters:

			# If there is a 'results'-type filter, convert it into a
			
			# Initialize list of conditions to be constructed from filters.
			conditions = []

			for f in filters:

				quote_values = False
				if isinstance(SASI_Result.columns[f['name']],pytables.description.StringCol):
					quote_values = True

				filter_conditions = []
				for fv in f['values']:
					if quote_values: fv = "'%s'" % fv
					filter_conditions.append("(%s %s %s)" % (f['name'], f['operator'], fv))
				filter_conditions_string = ' | '.join(filter_conditions)

				conditions.append(filter_conditions_string)

			conditions_string = ' & '.join(["( %s )" % c for c in conditions])

			# Return iterable for filtered results.
			if as_proxy: return self.results_table.where(conditions_string)
			else: return self.results_table.readWhere(conditions_string)

		# Otherwise return iterable for all results.
		if as_proxy: return self.results_table.__iter__()
		else: return self.results_table.read()

	# Create new results.
	def create_results(self, results=None):
		for result in results:
			result_row = self.results_table.row
			for k,v in result.items():
				result_row[k] = v
			result_row['key'] = self.get_key_for_result(result)
			result_row.append()
		self.results_table.flush()

	def update_results(self, results=[]):

		# Fetch results.
		result_keys = [self.get_key_for_result(r) for r in results]
		fetched_results = self.get_results(
				filters = [
					{
						'name': 'key',
						'operator' : '==',
						'values' : result_keys
						},
					],
				as_proxy = True
				)

		# Update each result...
		i = 0
		for fetched_result in fetched_results:
			modified_result = results[i]
			for k,v in modified_result.items():
				fetched_result[k] = v
			fetched_result.update()
			i += 1

		# Flush updates to the table.
		self.results_table.flush()
