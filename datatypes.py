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
