MAP
    NAME "SASI Results Map"
	STATUS ON
    SIZE {{img_width}} {{img_height}}

	# SASI Model Domain, extended to account for rotation by -38d.
    EXTENT -82.16 30.0638 -62.0380 46.1056
	ANGLE -38.0

	PROJECTION
		"init=epsg:4326"
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
    	NAME "Results Data"
		TYPE POLYGON
		{{field_data_source}}
		STATUS DEFAULT

		PROJECTION
			"init=epsg:4326"
		END

		# Start data color classes.
		{% for color_class in color_classes %}
		CLASS
			EXPRESSION ({{ color_class['criteria'] | join(' AND ')}})
			STYLE
				COLOR {{color_class['r']}} {{color_class['g']}} {{color_class['b']}}
			END
		END
		{% endfor %}
		# End data classes.

	END
	## End results data.

END # MAP
