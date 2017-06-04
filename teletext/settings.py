def apply(dict, **args):
	newdict = dict.copy()
	newdict.update(args)
	return newdict

def defaults(dict, **args):
	return apply(args, **dict)
