class VulnerabilityAssessment(object):

	def __init__(self, rows=[]):

		self.assessments = self.makeAssessmentsFromRows(rows)
	
	def makeAssessmentsFromRows(self, rows):
		# Save rows, keyed by (GEAR_CODE, SUBSTRATE_CODE, FEATURE_CODE,ENERGY)
		assessments = {}
		for r in rows:
			key = (r['GEAR_CODE'], r['SUBSTRATE_CODE'], r['FEATURE_CODE'], r['ENERGY'])
			assessments[key] = r
		return assessments

	def getFeaturesByHabitats(self):
		f_by_h = {}
		for key, assessment in self.assessments.items():
			hab_key = (assessment['SUBSTRATE_CODE'], assessment['ENERGY'])
			features_for_hab = f_by_h.setdefault(hab_key,{})
			features_for_category = features_for_hab.setdefault(assessment['FEATURE_CLASS_CODE'],set())
			features_for_category.add(assessment['FEATURE_CODE'])
		return f_by_h

	def getFeatures(self):
		features = {} 
		for key, assessment in self.assessments.items():
			features[assessment['FEATURE_CODE']] = {
					'FEATURE_CODE': assessment['FEATURE_CODE'],
					'FEATURE_CLASS_CODE': assessment['FEATURE_CLASS_CODE'],
					'FEATURE': assessment['FEATURE']
					}
		return features

