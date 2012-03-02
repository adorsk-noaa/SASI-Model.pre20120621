from sqlalchemy.sql import compiler

# Compile a query into raw sql.
def query_to_raw_sql(q):
	dialect = q.session.bind.dialect
	statement = q.statement
	comp = compiler.SQLCompiler(dialect, statement)
	comp.compile()
	enc = dialect.encoding
	params = {}
	for k,v in comp.params.iteritems():
		if isinstance(v, unicode):
			v = v.encode(enc)
		if isinstance(v, str):
			v = comp.render_literal_value(v, str)
		params[k] = v

	raw_sql = (comp.string.encode(enc) % params).decode(enc)
	return raw_sql
