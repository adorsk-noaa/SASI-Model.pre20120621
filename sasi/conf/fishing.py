# Define gear types.
gear_definitions = [
		{'name': 'Generic Trawl', 'id': 'GC1', 'category': 'Trawl'},
		{'name': 'Otter Trawl', 'id': 'GC10', 'category': 'Trawl'},
		{'name': 'Shrimp', 'id': 'GC11', 'category': 'Trawl'},
		{'name': 'Squid', 'id': 'GC12', 'category': 'Trawl'},
		{'name': 'Raised', 'id': 'GC13', 'category': 'Trawl'},
		{'name': 'Generic Scallop', 'id': 'GC2', 'category': 'Scallop'},
		{'name': 'Scallop Dredge, Limited Access', 'id': 'GC20', 'category': 'Scallop'},
		{'name': 'Scallop Dredge, General', 'id': 'GC21', 'category': 'Scallop'},
		{'name': 'Generic Dredge', 'id': 'GC3', 'category': 'Dredge'},
		{'name': 'Hydraulic Dredge', 'id': 'GC30', 'category': 'Dredge'},
		{'name': 'Generic Longline', 'id': 'GC4', 'category': 'Longline'},
		{'name': 'Longline', 'id': 'GC40', 'category': 'Longline'},
		{'name': 'Generic Gillnet', 'id': 'GC5', 'category': 'Gillnet'},
		{'name': 'Gillnet', 'id': 'GC50', 'category': 'Gillnet'},
		{'name': 'Generic Trap', 'id': 'GC6', 'category': 'Trap'},
		{'name': 'Trap', 'id': 'GC60', 'category': 'Trap'},
		]
		
# Map gear categories to VA dry codes.
gear_category_to_dry_code = {
		'Trawl': 'GC1',
		'Scallop': 'GC2',
		'Dredge': 'GC3',
		'Longline': 'GC4',
		'Gillnet': 'GC5',
		'Trap': 'GC6',
		}

# Create inverse mapping.
dry_code_to_gear_category = {}
for gcat, dry_code in gear_category_to_dry_code.items():
	dry_code_to_gear_category[dry_code] = gcat


