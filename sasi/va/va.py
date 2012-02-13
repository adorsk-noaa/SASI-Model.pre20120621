class VulnerabilityAssessment(object):

	def __init__(self, rows=[]):

		self.assessments = self.make_assessments_from_rows(rows)
	
	def make_assessments_from_rows(self, rows):
		# Save rows, keyed by (GEAR_CODE, SUBSTRATE_CODE, FEATURE_CODE,ENERGY)
		assessments = {}
		for r in rows:

			# Map energy to numerical strings.
			if r['ENERGY'] == 'High': r['ENERGY'] = '1.0'
			else: r['ENERGY'] = '0.0'

			key = (r['GEAR_CODE'], r['SUBSTRATE_CODE'], r['FEATURE_CODE'], r['ENERGY'])
			assessments[key] = r

		return assessments

	def get_assessment(self, gear_code='', substrate_code='', feature_code='', energy=''):
		key = (gear_code, substrate_code, feature_code, energy)
		return self.assessments.get(key, None)

	def get_susceptibility(self, **kwopts):
		assessment = self.get_assessment(**kwopts)
		if assessment:
			return assessment['S']


	def get_recovery(self, **kwopts):
		assessment = self.get_assessment(**kwopts)
		if assessment:
			return assessment['R']

	def get_features_by_habitats(self):
		f_by_h = {}
		for key, assessment in self.assessments.items():
			hab_key = (assessment['SUBSTRATE_CODE'], assessment['ENERGY'])
			features_for_hab = f_by_h.setdefault(hab_key,{})
			features_for_category = features_for_hab.setdefault(assessment['FEATURE_CLASS_CODE'],set())
			features_for_category.add(assessment['FEATURE_CODE'])
		return f_by_h

	def get_features(self):
		features = {} 
		for key, assessment in self.assessments.items():
			features[assessment['FEATURE_CODE']] = {
					'FEATURE_CODE': assessment['FEATURE_CODE'],
					'FEATURE_CLASS_CODE': assessment['FEATURE_CLASS_CODE'],
					'FEATURE': assessment['FEATURE']
					}
		return features
	
	def get_substrates(self):
		substrates = {} 
		for key, assessment in self.assessments.items():
			substrates[assessment['SUBSTRATE_CODE']] = {
					'SUBSTRATE_CODE': assessment['SUBSTRATE_CODE'],
					'SUBSTRATE': assessment['SUBSTRATE']
					}
		return substrates


	def get_gears_by_habitats(self):
		g_by_h = {}
		for key, assessment in self.assessments.items():
			hab_key = (assessment['SUBSTRATE_CODE'], assessment['ENERGY'])
			gears_for_hab = g_by_h.setdefault(hab_key,set())
			gears_for_hab.add(assessment['GEAR_CODE'])
		return g_by_h
	
	def get_habitats_by_gears(self):
		h_by_g = {}
		for key, assessment in self.assessments.items():
			hab_key = (assessment['SUBSTRATE_CODE'], assessment['ENERGY'])
			habs_for_gears= h_by_g.setdefault(assessment['GEAR_CODE'], set())
			habs_for_gears.add(hab_key)
		return h_by_g

	def get_features_by_gears(self):
		f_by_g = {}
		for key, assessment in self.assessments.items():
			features_for_gears = f_by_g.setdefault(assessment['GEAR_CODE'], set())
			features_for_gears.add(assessment['FEATURE_CODE'])
		return f_by_g

	def get_habitats_for_gear(self, gear_code):
		habitats = set()
		for key, assessment in self.assessments.items():
			if assessment['GEAR_CODE'] == gear_code:
				hab_key = (assessment['SUBSTRATE_CODE'], assessment['ENERGY'])
				habitats.add(hab_key)
		return habitats

	def get_features_for_gear(self, gear_code):
		features = set()
		for key, assessment in self.assessments.items():
			if assessment['GEAR_CODE'] == gear_code:
				features.add(assessment['FEATURE_CODE'])
		return features

	def get_gears(self):
		gears = {} 
		for key, assessment in self.assessments.items():
			gears[assessment['GEAR_CODE']] = {
					'GEAR_CODE': assessment['GEAR_CODE'],
					'GEAR': assessment['GEAR']
					}
		return gears

	def get_habitats(self):
		habitats = set()
		for key, assessment in self.assessments.items():
			hab_key = (assessment['SUBSTRATE_CODE'], assessment['ENERGY'])
			habitats.add(hab_key)
		return habitats

