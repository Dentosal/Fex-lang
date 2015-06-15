"""
corefunctions contains functions that define minimal core of language, such as:

implemented:
	* Simple math: [neq, add, sub, mul, div, idiv, mod, imod]
	* Simple logic: [eq, ne, lt, gt, lte, gte, and, or]
	* List generation: [range, list]
	* Array operations: [set_at, get_at, del_at, count, length]
missing:
	* Type conversions: [int, str, flt, lst]
	* Flow Control: [if, while, repeat]


Functions `import` and `exit` are implemented straight into interpreter.

"""
import re
import sys

import datatypes
from meta import error, AbortExecution

# simple math operations
def f_neq(args):
	if len(args) != 1:
		error("Invalid number of arguments (%s) for '%s'" % (0, "neq"))
	if isinstance(args[0], datatypes.Integer):
		return datatypes.Integer(-args[0].value)
	elif isinstance(args[0], datatypes.Float):
		return datatypes.Float(-args[0].value)
	elif isinstance(args[0], datatypes.String):	# reverse; neq("Hello") -> "olleH"
		return datatypes.String(args[0].value[::-1])
	else:
		error("Unsupported operand for '%s' with basetype '%s': '%s'" % ("neq", basetype, args[0].TYPE))
def f_abs(args):
	if len(args) != 1:
		error("Invalid number of arguments (%s) for '%s'" % (0, "neq"))
	if isinstance(args[0], datatypes.Integer):
		return datatypes.Integer(abs(args[0].value))
	elif isinstance(args[0], datatypes.Float):
		return datatypes.Float(abs(args[0].value))
	else:
		error("Unsupported operand for '%s' with basetype '%s': '%s'" % ("neq", basetype, args[0].TYPE))
def f_add(args):
	""" Add function (also sum function) """
	if len(args) == 0:
		error("Invalid number of arguments (%s) for '%s'" % (0, "add"))
	elif len(args) == 1:
		if isinstance(args[0], datatypes.List):
			return f_add(args[0].value)
		else:
			return args[0]

	# take base item
	basetype = args[0].TYPE
	basevalue = args[0].value

	if basetype == "list":
		for a in args[1:]:
			if isinstance(a, datatypes.Integer) or isinstance(a, datatypes.Float) or isinstance(a, datatypes.String):
				basevalue.append(a)
			elif isinstance(a, datatypes.List):
				basevalue += a.value
			else:
				error("Unsupported operand for '%s' with basetype '%s': '%s'" % ("add", basetype, a.TYPE))
		return datatypes.List(basevalue)
	elif basetype in ["float", "integer"]:
		for a in args[1:]:
			if isinstance(a, datatypes.Integer) or isinstance(a, datatypes.Float):
				basevalue += a.value
			else:
				error("Unsupported operand for '%s' with basetype '%s': '%s'" % ("add", basetype, a.TYPE))
		return datatypes.Integer(basevalue) if int(basevalue) == basevalue else datatypes.Float(basevalue)
	elif basetype == "string":
		print args[0]
		for a in args[1:]:
			if isinstance(a, datatypes.String) or isinstance(a, datatypes.Integer) or isinstance(a, datatypes.Float):
				basevalue += str(a.value)
			else:
				error("Unsupported operand for '%s' with basetype '%s': '%s'" % ("add", basetype, a.TYPE))
		return datatypes.String(basevalue)
	else:
		error("Unsupported basetype '%s' for '%s'" % (basetype, "add"))
def f_sub(args):
	if len(args) != 2:
		error("Invalid number of arguments (%s) for '%s'" % (len(args), "sub"))

	# take base item
	basetype = args[0].TYPE
	basevalue = args[0].value

	if basetype in ["float", "integer"] and (isinstance(args[1], datatypes.Integer) or isinstance(args[1], datatypes.Float)):
		basevalue += args[1].value
		return datatypes.Integer(basevalue) if int(basevalue) == basevalue else datatypes.Float(basevalue)
	else:
		error("Unsupported basetype '%s' for '%s'" % (basetype, "sub"))
def f_mul(args):
	if len(args) == 0:
		error("Invalid number of arguments (%s) for '%s'" % (0, "mul"))
	elif len(args) == 1:
		if isinstance(args[0], datatypes.List):
			return f_mul(args[0].value)
		else:
			return args[0]

	# take base item
	basetype = args[0].TYPE
	basevalue = args[0].value

	if basetype == "list":
		for a in args[1:]:
			if isinstance(a, datatypes.Integer):
				basevalue *= a.value
			else:
				error("Unsupported operand for '%s' with basetype '%s': '%s'" % ("mul", basetype, a.TYPE))
		return datatypes.List(basevalue)
	elif basetype in ["float", "integer"]:
		for a in args[1:]:
			if isinstance(a, datatypes.Integer) or isinstance(a, datatypes.Float):
				basevalue *= a.value
			else:
				error("Unsupported operand for '%s' with basetype '%s': '%s'" % ("mul", basetype, a.TYPE))
		return datatypes.Integer(basevalue) if int(basevalue) == basevalue else datatypes.Float(basevalue)
	elif basetype == "string":
		print args[0]
		for a in args[1:]:
			if isinstance(a, datatypes.Integer):
				basevalue *= a.value
			else:
				error("Unsupported operand for '%s' with basetype '%s': '%s'" % ("mul", basetype, a.TYPE))
		return datatypes.String(basevalue)
	else:
		error("Unsupported basetype '%s' for '%s'" % (basetype, "mul"))
def f_idiv(args):
	""" Integer division. """
	if len(args) != 2:
		error("Invalid number of arguments (%s) for '%s'" % (len(args), "idiv"))

	if isinstance(args[0], datatypes.Integer) and isinstance(args[1], datatypes.Integer):
		return datatypes.Integer(int(args[0].value/args[1].value))
	else:
		error("Unsupported types '%s' and '%s' for '%s'" % (args[0].TYPE, args[1].TYPE, "idiv"))
def f_div(args):
	""" 'Normal' (or 'Pythonic') division. """
	if len(args) != 2:
		error("Invalid number of arguments (%s) for '%s'" % (len(args), "div"))

	if (isinstance(args[0], datatypes.Integer) or isinstance(args[0], datatypes.Float)) and (isinstance(args[1], datatypes.Integer) or isinstance(args[1], datatypes.Float)):
		ret = float(args[0].value)/float(args[1].value)
		return datatypes.Integer(ret) if int(ret) == ret else datatypes.Float(ret)
	else:
		error("Unsupported types '%s' and '%s' for '%s'" % (args[0].TYPE, args[1].TYPE, "div"))
def f_imod(args):
	""" Integer modulo. """
	if len(args) != 2:
		error("Invalid number of arguments (%s) for '%s'" % (len(args), "mod"))

	if isinstance(args[0], datatypes.Integer) and isinstance(args[1], datatypes.Integer):
		return datatypes.Integer(int(args[0].value%args[1].value))
	else:
		error("Unsupported types '%s' and '%s' for '%s'" % (args[0].TYPE, args[1].TYPE, "imod"))
def f_mod(args):
	""" ('Pythonic') Modulo that works with float. """
	if len(args) != 2:
		error("Invalid number of arguments (%s) for '%s'" % (len(args), "mod"))

	if isinstance(args[0], datatypes.Integer) and isinstance(args[1], datatypes.Integer):
		return datatypes.Integer(int(args[0].value%args[1].value))
	elif (isinstance(args[0], datatypes.Integer) or isinstance(args[0], datatypes.Float)) and (isinstance(args[1], datatypes.Integer) or isinstance(args[1], datatypes.Float)):
		ret = float(args[0].value)%float(args[1].value)
		return datatypes.Integer(ret) if int(ret) == ret else datatypes.Float(ret)
	else:
		error("Unsupported types '%s' and '%s' for '%s'" % (args[0].TYPE, args[1].TYPE, "mod"))

# boolean logic
def f_and(args):
	""" Boolean AND. Also `all`-function from python. """
	if len(args) == 0:
		error("Invalid number of arguments (%s) for '%s'" % (len(args), "and"))
	for i in range(len(args)):
		if not (isinstance(args[i], datatypes.Integer) or isinstance(args[i], datatypes.Float)):
			error("Unsupported type '%s' for '%s'" % (args[i].TYPE, "and"))
		args[i] = bool(int(args[i].value))
	return datatypes.Integer(all(args))
def f_or(args):
	""" Boolean OR. Also `any`-function from python. """
	if len(args) == 0:
		error("Invalid number of arguments (%s) for '%s'" % (len(args), "or"))
	for i in range(len(args)):
		if not (isinstance(args[i], datatypes.Integer) or isinstance(args[i], datatypes.Float)):
			error("Unsupported type '%s' for '%s'" % (args[i].TYPE, "or"))
		args[i] = bool(int(args[i].value))
	return datatypes.Integer(any(args))



# comparisons
def compare(a, b):
	""" Internal function: compare two items.
		Return: ["=", "<", ">"]
	"""
	if isinstance(a, datatypes.String):
		if isinstance(b, datatypes.String):
			return ["><"[a.value<b.value], "="][a.value==b.value]
		else:
			error("Cannot compare '%s' and '%s'" % (a.TYPE, b.TYPE))
	elif isinstance(a, datatypes.Integer) or isinstance(a, datatypes.Float):
		if isinstance(b, datatypes.Integer) or isinstance(b, datatypes.Integer):
			return ["><"[a.value<b.value], "="][a.value==b.value]
		else:
			error("Cannot compare '%s' and '%s'" % (a.TYPE, b.TYPE))
	elif isinstance(a, datatypes.Symbol):
		error("Cannot compare '%s' and '%s'" % (a.TYPE, b.TYPE))
	elif isinstance(a, datatypes.List):
		if isinstance(b, datatypes.List):
			for ind in range(min(len(a.value), len(b.value))):
				c = compare(a.value[ind], b.value[ind])
				if c != "=":
					return c
			return ["><"[len(a.value)<len(b.value)], "="][len(a.value)==len(b.value)]
		else:
			error("Cannot compare '%s' and '%s'" % (a.TYPE, b.TYPE))
	else:
		error("Interpreter Error: Compare: Unknown type '%s'" % base.TYPE)

def f_eq(args):
	"""" allows multiple parameters and test are they all are same """
	if len(args) == 1 and isinstance(args[0], datatypes.List):
		return f_eq(args[0])
	if len(args) < 2:
		error("Invalid number of arguments (%s) for '%s'" % (len(args), "compare"))
	base = args[0]
	for a in args[1:]:
		if compare(base, a) != "=":
			return datatypes.Integer(False)
	return datatypes.Integer(True)

def f_ne(args):
	""" not equals """
	return datatypes.Integer(not f_eq(args).value)
def f_lt(args):
	""" allows multiple parameters and test are they sorted to ascending order (no equalities allowed) """
	if len(args) == 1 and isinstance(args[0], datatypes.List):
		return f_lt(args[0])
	if len(args) < 2:
		error("Invalid number of arguments (%s) for '%s'" % (len(args), "lt"))
	base = args[0]
	curr = args[0]
	for a in args[1:]:
		if compare(curr, a) != "<":
			return datatypes.Integer(False)
		curr = a
	return datatypes.Integer(True)
def f_lte(args):
	""" allows multiple parameters and test are they sorted to ascending order (equalities allowed) """
	if len(args) == 1 and isinstance(args[0], datatypes.List):
		return f_lte(args[0])
	if len(args) < 2:
		error("Invalid number of arguments (%s) for '%s'" % (len(args), "lte"))
	base = args[0]
	curr = args[0]
	for a in args[1:]:
		if compare(curr, a) == ">":
			return datatypes.Integer(False)
		curr = a
	return datatypes.Integer(True)
def f_gt(args):
	""" allows multiple parameters and test are they sorted to descending order (no equalities allowed) """
	if len(args) == 1 and isinstance(args[0], datatypes.List):
		return f_gt(args[0])
	if len(args) < 2:
		error("Invalid number of arguments (%s) for '%s'" % (len(args), "gt"))
	base = args[0]
	curr = args[0]
	for a in args[1:]:
		if compare(curr, a) != ">":
			return datatypes.Integer(False)
		curr = a
	return datatypes.Integer(True)
def f_gte(args):
	""" allows multiple parameters and test are they sorted to descending order (equalities allowed) """
	if len(args) == 1 and isinstance(args[0], datatypes.List):
		return f_gte(args[0])
	if len(args) < 2:
		error("Invalid number of arguments (%s) for '%s'" % (len(args), "gte"))
	base = args[0]
	curr = args[0]
	for a in args[1:]:
		if compare(curr, a) == "<":
			return datatypes.Integer(False)
		curr = a
	return datatypes.Integer(True)

# object creation
def f_list(args):
	""" Create list. list(1, 2, 3) is same as [1, 2, 3] """
	return datatypes.List(args)
def f_range(args):
	""" Pythonic range function """
	if not len(args) in [1, 2, 3]:
		error("Invalid number of arguments (%s) for '%s'" % (len(args), "range"))
	if all([isinstance(a, datatypes.Integer) for a in args]):
		return datatypes.List([datatypes.Integer(i) for i in range(*[a.value for a in args])])	# unpack arguments form list
	else:
		error("Function '%s' takes Integer arguments only." % "range")

# array (list and string) related
def f_get_at(args):
	""" Get item at index """
	if len(args) != 2:
		error("Invalid number of arguments (%s) for '%s'" % (len(args), "get_at"))
	array, index = args
	if not (isinstance(array, datatypes.String) or isinstance(array, datatypes.List)):
		error("Invalid argument for '%s': Array must be Sting or List, got '%s'." % ("get_at", array.TYPE))
	if not isinstance(index, datatypes.Integer):
		error("Invalid argument for '%s': Index must be Integer, got '%s'." % ("get_at", index.TYPE))
	try:
		ret = array.value[index.value]
	except IndexError:
		error("%s index out of range in function '%s'" % (array.TYPE, "get_at"))
	if isinstance(array, datatypes.String):
		return datatypes.String(ret)
	else:
		return ret
def f_set_at(args):
	""" Set item at index """
	if len(args) != 3:
		error("Invalid number of arguments (%s) for '%s'" % (len(args), "set_at"))
	array, index, new_item = args
	if not (isinstance(array, datatypes.String) or isinstance(array, datatypes.List)):
		error("Invalid argument for '%s': Array must be Sting or List, got '%s'." % ("set_at", array.TYPE))
	if not isinstance(index, datatypes.Integer):
		error("Invalid argument for '%s': Index must be Integer, got '%s'." % ("set_at", index.TYPE))
	if isinstance(array, datatypes.String):
		if not isinstance(new_item, datatypes.String):
			error("Invalid argument for '%s': Part of String must be replaced with String." % ("set_at"))
		ret = list(array.value)
		try:
			del ret[index.value]
		except IndexError:
			error("String index out of range in function '%s'" % "set_at")
		if new_item.value != "":
			ret.insert(list(new_item.value))
		return datatypes.String(ret)
	else:
		try:
			array.value[index.value] = new_item
		except IndexError:
			error("List index out of range in function '%s'" % "set_at")
		return array
def f_del_at(args):
	""" Del item at index """
	if len(args) != 2:
		error("Invalid number of arguments (%s) for '%s'" % (len(args), "del_at"))
	array, index = args
	if not (isinstance(array, datatypes.String) or isinstance(array, datatypes.List)):
		error("Invalid argument for '%s': Array must be Sting or List, got '%s'." % ("del_at", array.TYPE))
	if not isinstance(index, datatypes.Integer):
		error("Invalid argument for '%s': Index must be Integer, got '%s'." % ("del_at", index.TYPE))
	if isinstance(array, datatypes.String):
		ret = list(array.value)
		try:
			del ret[index.value]
		except IndexError:
			error("String index out of range in function '%s'" % "del_at")
		return datatypes.String(ret)
	else:
		try:
			del array.value[index.value]
		except IndexError:
			error("List index out of range in function '%s'" % "det_at")
		return array
def f_length(args):
	if len(args) != 1:
		error("Invalid number of arguments (%s) for '%s'" % (len(args), "length"))
	if not (isinstance(args[0], datatypes.String) or isinstance(args[0], datatypes.List)):
		error("Invalid argument for '%s': Array must be Sting or List, got '%s'." % ("length", array.TYPE))
	else:
		return len(args[0].value)
def f_count(args):
	""" Set item at index """
	if len(args) != 2:
		error("Invalid number of arguments (%s) for '%s'" % (len(args), "count"))
	array, item = args
	if not (isinstance(array, datatypes.String) or isinstance(array, datatypes.List)):
		error("Invalid argument for '%s': Array must be Sting or List, got '%s'." % ("count", array.TYPE))
	if isinstance(array, datatypes.String):
		if isinstance(item, datatypes.String):
			error("Invalid argument for '%s': you can only count Strings in String." % ("count"))
		return datatypes.Integer(array.value.count(item.value))
	else:
		ret = 0
		for av in array.value:
			if f_eq([av, item]):
				ret += 1
		return datatypes.Integer(ret)

# type conversions
def f_int(args):
	if len(args) != 1:
		error("Invalid number of arguments (%s) for '%s'" % (len(args), "int"))
	if isinstance(args[0], datatypes.Integer) or isinstance(args[0], datatypes.Float):
		return datatypes.Integer(args[0].value)
	elif isinstance(args[0], datatypes.String):
		if re.findall("^\\d+$", args[0].value) != []:
			return datatypes.Integer(args[0].value)
		else:
			error("Invalid literal for '%s': '%s'" % ("int", args[0].value))
	else:
		error("Cannot convert from type '%s' to '%s'" % (args[0].TYPE, "integer"))
def f_flt(args):
	if len(args) != 1:
		error("Invalid number of arguments (%s) for '%s'" % (len(args), "flt"))
	if isinstance(args[0], datatypes.Integer) or isinstance(args[0], datatypes.Float):
		return datatypes.Float(args[0].value)
	elif isinstance(args[0], datatypes.String):
		if re.findall("^\\d+.\\d+$", args[0].value) != [] or re.findall("^\\d+$", args[0].value) != []:
			return datatypes.Float(args[0].value)
		else:
			error("Invalid literal for '%s': '%s'" % ("flt", args[0].value))
	else:
		error("Cannot convert from type '%s' to '%s'" % (args[0].TYPE, "float"))
def f_str(args):
	if len(args) != 1:
		error("Invalid number of arguments (%s) for '%s'" % (len(args), "str"))
	if isinstance(args[0], datatypes.Integer) or isinstance(args[0], datatypes.Float) or isinstance(args[0], datatypes.String):
		return datatypes.String(args[0].value)
	elif isinstance(args[0], datatypes.List):
		return datatypes.String(datatypes.format_to_string(args[0]))
	else:
		error("Cannot convert from type '%s' to '%s'" % (args[0].TYPE, "string"))

# aliases
f_sum = f_add
f_len = f_length
f_all = f_and
f_any = f_or
