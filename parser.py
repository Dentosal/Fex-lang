import datatypes
from meta import Token, AbortExecution, error

def dectectTokenType(symbol, line):
	if symbol[0] == "\"":
		return "string"
	elif re.match("\\-?[0-9]+$", symbol):
		return "integer"
	elif len(symbol) > 1 and re.match("\\-?[0-9]*\\.[0-9]*$", symbol):
		return "float"
	elif re.match("^[a-zA-Z_][a-zA-Z0-9_\\.]*$", symbol) and symbol[-1] != ".":
		return "symbol"
	elif symbol in list("([{}]),"):
		return {"(": "args_start", ")": "args_end", "{": "block_start", "}": "block_end",
				"[": "symbol_start", "]": "symbol_end", ",": "arg_separator"}[symbol]
	else:
		error("Invalid object '%s' in line %i" % (symbol, line))

        def parse(source):
        	tokens = []
        	strings = []
        	# process source line-by-line and create token list
        	for lineIndex in range(len(source)):
        		line = source[lineIndex]
        		# collect strings
        		for i in re.findall("(\"\"|\".*?[^\\\\]\")", line):
        			w = i.replace("\\n", "\n").replace("\\r", "\r").replace("\\t", "\t").replace("\\\"", "\"")
        			strings.append(w)
        			line = line.replace(w, " \" ")
        		# add spaces
        		for c in list("([{}]),"):
        			line = line.replace(c, " "+c+" ")
        		# split
        		for t in line.split():
        			tokens.append(Token(t, lineIndex+1))
        	# put strings back to tokens and handle other token values as well
        	for t in range(len(tokens)):
        		if tokens[t].type == "string":
        			tokens[t].value = datatypes.String(strings[0][1:-1])
        			strings = strings[1:]
        		elif tokens[t].type == "integer":
        			tokens[t].value = datatypes.Integer(tokens[t].data)
        		elif tokens[t].type == "float":
        			tokens[t].value = datatypes.Float(tokens[t].data)
        		elif tokens[t].type == "symbol":
        			tokens[t].value = datatypes.Symbol(tokens[t].data)

        	return tokens
