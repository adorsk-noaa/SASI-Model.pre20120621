"""
Layer definitions for map base layers.
"""
coastline = """
    LAYER
        NAME "Coastline"
        TYPE POLYGON
        DATA !!!!
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
				LINEWIDTH
			END
		END
	"""

state_boundaries = """
    LAYER
        NAME "State Boundaries"
        TYPE POLYGON
        DATA !!!!
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
				OUTLINECOLOR 32 32 32
				COLOR 232 232 232
			END
		END
	"""
eez = """
    LAYER
        NAME "EEZ"
        TYPE POLYGON
        DATA !!!!
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
				OUTLINECOLOR 32 32 32
				COLOR 232 232 232
			END
		END
	"""

sasi_domain_boundary = """
    LAYER
        NAME "SASI Domain Outline"
        TYPE POLYGON
        DATA !!!!
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

    END # SASI Domain Outline 
"""

