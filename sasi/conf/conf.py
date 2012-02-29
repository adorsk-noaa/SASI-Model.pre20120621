import sasi.conf.secrets as secrets

conf = {
		'grid_file': '/home/adorsk/projects/sasi/data/Final_SASI_GIS/Standard_Grids.shp',
		'va_file': '/home/adorsk/projects/sasi/data/vulnerability_assessment/matrices_master.csv',
		'sasi_habitat_file': '/home/adorsk/projects/sasi/data/Final_SASI_GIS/Grid_SASI.shp',
		'verbose': False,
		'output_dir': '/home/adorsk/projects/sasi/sasi_model/outputs,'
		}

# Add in secrets.
conf.update(secrets.secrets)
