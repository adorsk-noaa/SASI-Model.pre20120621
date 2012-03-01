MAP
    NAME "SASI Results Map"
	STATUS ON
    SIZE {{img_width}} {{img_height}}

	# SASI Model Domain, extended to account for rotation by -38d.
    EXTENT -82.16 30.0638 -62.0380 46.1056
	ANGLE -38.0

	PROJECTION
		"proj=longlat"
		"ellps=GRS80"
		"datum=NAD83"
		"no_defs"
    END
	
	OUTPUTFORMAT
	  NAME "png"
	  DRIVER AGG/PNG
	  MIMETYPE "image/png"
	  IMAGEMODE RGB
	  EXTENSION "png"
	END

    #
    # Start of layer definitions
    #
	{% for base_layer in base_layers %}
		{{base_layer}}

    {% endfor %}
	
	# Start results data.
	LAYER
    	NAME "Results Data: {{field}}"
		TYPE POLYGON
		{{field_data_source}}
		STATUS DEFAULT

		PROJECTION
			"proj=utm"
			"ellps=GRS80"
			"datum=NAD83"
			"no_defs"
			"units=m"
			"zone=19"
		END

		# Start data color classes.
		{% for color_class in color_classes %}
		CLASS
			NAME "{{color_class.name}}"
			EXPRESSION ({% for crit in color_class.criteria%} ("{{field}}" {{crit.op}} {{crit.value}}) {% endfor %})
			STYLE
				COLOR {{crit.red}} {{crit.green}} {{crit.blue}}
			END
		END
		{% endfor %}
		# End data classes.

	END
	## End results data.

END # MAP
