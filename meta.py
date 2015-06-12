# Meta does not import any of other project files.
# Thats why it's possible to import it to every file.

import re
def dectectTokenType(symbol, line):
	if symbol[0] == "\"":
		return "string"
	elif re.match("\\-?[0-9]+$", symbol):
		return "integer"
	elif len(symbol) > 1 and re.match("\\-?[0-9]+\\.[0-9]+$", symbol):
		return "float"
	elif re.match("^[a-zA-Z_][a-zA-Z0-9_\\.]*$", symbol) and symbol[-1] != ".":
		return "symbol"
	elif symbol in list("([{}]),"):
		return {"(": "args_start", ")": "args_end", "{": "block_start", "}": "block_end",
				"[": "symbol_start", "]": "symbol_end", ",": "arg_separator"}[symbol]
	else:
		error("Invalid object '%s' in line %i" % (symbol, line))

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
