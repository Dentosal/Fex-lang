from meta import error
class Datatype:
	TYPE = "data"
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return "%s(%s)" % (self.TYPE, str(self.value))
	def __repr__(self):
		return "%s(%s)" % (self.TYPE, str(self.value))

class Symbol(Datatype):
	TYPE = "symbol"
	def __init__(self, value):
		self.value = str(value)

class Integer(Datatype):
	TYPE = "integer"
	def __init__(self, value):
		self.value = int(value)
class Float(Datatype):
	TYPE = "float"
	def __init__(self, value):
		self.value = float(value)

class String(Datatype):
	TYPE = "string"
	def __init__(self, value):
		self.value = str(value)

class List(Datatype):
	TYPE = "list"
	def __init__(self, value):
		self.value = value

class Function:
	TYPE = "function"
	FTYPE = "" # function call type: "python" or "fex"
	def call(self, args):
		pass
class PythonFunction(Function):
	FTYPE = "python"
	def __init__(self, function):
		self.function = function
	def call(self, args):
		return self.function(args)



# representation functions

def string_escape(S):
	if type(s) == type(""):
		return S.replace("\t", "\\t").replace("\n", "\\n").replace("\r", "\\r").replace("\"", "\\\"").replace("\\\\", "\\")
	elif isinstance(S, String):
		return string_escape(S.value)
	else:
		raise ValueError("Invalid convert.")

def format_modify_for_type(S, T):
	""" Special formatting, just like python's __repr__, but function, not method """
	if T == "string":
		S = "\"" + S.__repr__()[1:-1] + "\""
	return S

def format_to_string(item):
	""" Formats value of object to printable string. """
	if isinstance(item, String) or isinstance(item, Integer) or isinstance(item, Float):
		return str(item.value)
	elif isinstance(item, List):
		return "[" + (", ".join([format_modify_for_type(format_to_string(i), i.TYPE) for i in item.value])) + "]"
	else:
		error("Unsupported type '%s' for '%s'" % (item.TYPE, "string_format"))
