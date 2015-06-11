class Token:
	def __init__(self, data, linenumber):
		self.data = data
		self.line = int(linenumber)
		self.type = dectectTokenType(self.data, self.line)
		self.value = None
	def __repr__(self):
		return "Symbol '%s':'%s' at line %i" % (self.type, self.value if self.value != None else self.data, self.line)


class AbortExecution(Exception):
	pass

def error(msg):
	print "Error:", msg
	raise AbortExecution
