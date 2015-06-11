import re
import os
import sys


import datatypes
from meta import Token, AbortExecution, error

import corefunctions

NO_VARIABLE_INSERT_TOKENS = ["__symbol__", "__block__"]




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

def call_function(function, args, namespace):
	# in-complier functions (currently cannot be overwrited)
	if expr[0] == "exit":
		if len(args) == 0:
			sys.exit(0)
		elif len(args) == 1:
			if isinstance(args[0], datatypes.Integer):
				sys.exit(args[0].value)
			else:
				error("Invalid exid code type '%s'." % args[0].TYPE)
		else:
			error("exit(): invalid number of arguments: %i" % len(args))

	# TODO: test function in namespace

	# from corefunctions
	try:
		res = getattr(corefunctions, 'f_'+expr[0])(expr[1])
		return res, namespace
	except AttributeError:
		pass

	# function not found
	error("No function named '%s'." % expr[0])

def execute(expr, namespace):
	try:
		if len(expr) != 2:
			error("Invalid expression 1. (TODO)")
	except:
		error("Invalid expression 2. (TODO)")

	for i in range(len(expr[1])):
		if type(expr[1][i]) == type([]):
			expr[1][i], namespace = execute(expr[1][i], namespace)
		# convert tokens to `Datatype` objects
		if isinstance(expr[1][i], Token):
			expr[1][i] = expr[1][i].value

	return call_function(expr[0], expr[1], namespace)


def run_file(filename):
	with open(filename) as fo:
		contents = fo.read().replace("\r\n", "").split("\n")
	code = organise(parse(contents))
	namespace = {"__file__":filename}
	for expr in code:
		res, namespace = execute(expr, namespace)
#		namespace["_"] = res[0]

def run_ia():
	""" interactive interpreter """
	print "Interactive interpreter:"
	namespace = {"__file__": "<interactive>"}
	while True:
		inp = raw_input(">>> ").strip()
		if inp == "":
			continue
		if inp[0] == "!":
			if inp[1:] == "exit":
				sys.exit(0)
			elif inp[1:] == "ns":
				print namespace
			elif inp[1:] == "clear":
				os.system("clear")
			else:
				print "Invalid interactive interpreter instruction."
			continue
		try:
			res, namespace = execute(organise(parse([inp]))[0], namespace)
		except:
			pass
		else:
			print res



if __name__=="__main__":
	# find sourcefile
	no_prefix_args = [i for i in sys.argv[1:] if i[0]!="-"]
	if len(no_prefix_args) == 0: # no sourcefile -> interactive
		run_ia()
	else:	# run source file
		try:
			run_file(no_prefix_args[0])
		except AbortExecution:
			sys.exit(1)
