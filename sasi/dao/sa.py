# Common SQLALchemy DAO functions.

# Get mapserver connection string.
def get_mapserver_connection_string(sa_dao=None):

	# Get engine associated with the session.
	engine = sa_dao.session.bind.engine

	# Map mapserver connection parts to SA's url elements.
	mapserver_to_sa = {
			"host": "host",
			"dbname" : "database",
			"user": "username",
			"password": "password",
			"port": "port"
			}

	# Add connection parts if present.
	connection_parts = []
	for ms_name, sa_name in mapserver_to_sa.items():
		sa_value = getattr(engine.url, sa_name)
		if sa_value: connection_parts.append("%s=%s" % (ms_name, sa_value))

	# Return the combined connection string.
	return " ".join(connection_parts)
