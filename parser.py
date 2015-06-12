import re
import datatypes
from meta import Token, AbortExecution, error, dectectTokenType


def parse(source):
	tokens = []
	strings = []
	# process source line-by-line and create token list
	for lineIndex in range(len(source)):
		line = source[lineIndex]
		# collect strings (regex will not work, believe me, I have tried --Dentosal)
		string_start_index = None
		in_string = False
		escape_mode = False
		string = ""
		ind = 0
		while ind < len(line):
			c = line[ind]
			if in_string:
				if escape_mode == False:
					if c == "\\":
						escape_mode = True
					else:
						string += c
						if c == "\"":
							strings.append(string)
							line = list(line)
							line[string_start_index:ind+1] = " \" "
							line = "".join(line)
							in_string = False
				else:
					if not c in "\"\\nrt":
						error("Invalid escape inside string, line %i" % (lineIndex+1))
					string += {"\"": "\"", "\\": "\\", "n": "\n", "t": "\t", "r": "\r"}[c]
					escape_mode = False
			else:
				if c == "\"":
					string = "\""
					in_string = True
					string_start_index = ind
			ind += 1

		if in_string:
			error("End of line while scanning string literal, line %i" % (lineIndex+1))

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


def parse_function_call(expr):
	if isinstance(expr, Token):
		return expr
	if len(expr) == 0:
		return None
	if len(expr) == 1:
		if expr[0].type in ["string", "integer", "float", "symbol"]:
			return expr[0]
		else:
			error("Invalid type '%s' for function call", expr[1].type)
	if expr[0].type != "symbol" or expr[1].type != "args_start" or expr[-1].type != "args_end":
		if expr[0].line == expr[-1].line:
			error("Invalid function call in line %i" % expr[0].line)
		else:
			error("Invalid function call from line %i to line %i" % (expr[0].line, expr[-1].line))
	fun_name = expr[0].data
	# iterate over arguments
	args = []
	i = 2
	while i < len(expr)-1:
		e = expr[i]
		if e.type in ["string", "integer", "float"]:
			args.append(e)
		elif e.type == "arg_separator":
			pass
		elif e.type == "symbol":
			if expr[i+1].type == "args_start":
				p_level = 0
				buffer = [expr[i]]
				i += 1
				while i < len(expr)-1:
					buffer.append(expr[i])
					if expr[i].type == "args_start":
						p_level += 1
					elif expr[i].type == "args_end":
						p_level -= 1
						if p_level == 0:
							break
					i += 1
				if p_level != 0:
					error("Unbalanced parenthesis in line %i" % expr[i].line)
				args.append(parse_function_call(buffer))
			else:
				args.append(e)
		else:
			error("Internal interpreter error.")
		i += 1
	return [fun_name, args]

def organise(code):
	# split to expressions
	expressions = []
	buffer = []
	p_level = 0
	for item in code:
		buffer.append(item)
		if item.type == "args_start":
			p_level += 1
		elif item.type == "args_end":
			p_level -= 1
			if p_level == 0:
				expressions.append(buffer)
				buffer = []
	expressions.append(buffer)
	expressions = [parse_function_call(e) for e in expressions if e != []]
	return expressions
