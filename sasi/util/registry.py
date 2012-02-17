object_registry = {}

def get_or_register_object(o, id_func=lambda obj: obj.id):
	o_class = o.__class__.__name__
	o_id = id_func(o)

	o_key = (o_class, o_id)

	if not object_registry.has_key(o_key):
		object_registry[o_key] = o

	return object_registry[o_key]
