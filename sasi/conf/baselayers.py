"""
Layer definitions for map base layers.
"""
data_dir = "/home/adorsk/projects/sasi/data/gis/baselayers"

coastline = """
	# Start Coastline.
    LAYER
        NAME "Coastline"
        TYPE POLYGON
        DATA %s/%s
		STATUS DEFAULT

		PROJECTION
			"proj=longlat"
			"ellps=GRS80"
			"datum=NAD83"
			"no_defs"
		END

		CLASS
			NAME "Coastline"
			STYLE
				OUTLINECOLOR 32 32 32
				COLOR 232 232 232
			END
		END
	END
	# End Coastline.
	""" % (data_dir, "simple_east_coast")

state_boundaries = """
	# Start State Boundaries.
    LAYER
        NAME "State Boundaries"
        TYPE LINE
		DATA %s/%s
		STATUS DEFAULT

		PROJECTION
			"proj=longlat"
			"ellps=GRS80"
			"datum=NAD83"
			"no_defs"
		END

		CLASS
			NAME "State Boundaries"
			STYLE
				COLOR 32 32 32
			END
		END
	END
	# End State Boundaries.
	""" % (data_dir, "state_bounds")

eez = """
	# Start EEZ.
    LAYER
        NAME "EEZ"
        TYPE LINE
        DATA %s/%s
		STATUS DEFAULT

		PROJECTION
			"proj=longlat"
			"ellps=GRS80"
			"datum=NAD83"
			"no_defs"
		END

		CLASS
			NAME "EEZ"
			STYLE
				COLOR 232 232 232
			END
		END
	END
	# End EEZ.
	""" % (data_dir, "useez")

sasi_domain_boundary = """
    LAYER
        NAME "SASI Domain Outline"
        TYPE POLYGON
        DATA %s/%s
		STATUS DEFAULT

		PROJECTION
			"proj=longlat"
			"ellps=GRS80"
			"datum=NAD83"
			"no_defs"
		END

		CLASS
			NAME "Domain Outline"
			STYLE
				OUTLINECOLOR 32 32 32
				COLOR 232 232 232
			END
		END
    END
	# End SASI Domain Outline 
	""" % (data_dir, "sasi_domain_outline")

