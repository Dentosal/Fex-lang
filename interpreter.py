import re
import os
import sys
import importlib



import datatypes
from meta import Token, AbortExecution, error

import parser

import corefunctions


def init_namespace_functions(namespace):
	# from corefunctions
	for function in [f for f in dir(corefunctions) if f.startswith("f_")]:
		namespace[function[2:]] = datatypes.PythonFunction(getattr(corefunctions, function))

	# from stdlib
	for file in [fn for fn in os.listdir("stdlib") if fn.endswith(".py")]:
		lib = importlib.import_module("stdlib."+file.split(".")[0])
		for function in [f for f in dir(lib) if f.startswith("f_")]:
			namespace[".".join([file.split(".")[0], function[2:]])] = datatypes.PythonFunction(getattr(lib, function))
	return namespace




def call_function(function, args, namespace):
	# in-compiler functions (currently cannot be overwrited)
	if function == "exit":
		if len(args) == 0:
			sys.exit(0)
		elif len(args) == 1:
			if isinstance(args[0], datatypes.Integer):
				sys.exit(args[0].value)
			else:
				error("Invalid exid code type '%s'." % args[0].TYPE)
		else:
			error("exit(): invalid number of arguments: %i" % len(args))
	elif function == "import":
		error("Intepreter Error: Function 'import' is not implemented")

	# test if function is in namespace
	if function in namespace.keys():
		if isinstance(namespace[function], datatypes.Function):
			return namespace[function].call(args), namespace
		else:
			error("Cannot call non-callable type '%s'" % namespace[function].TYPE)

	# function not found
	error("No function named '%s'." % function)

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
	code = parser.organise(parser.parse(contents))
	namespace = init_namespace_functions({"__file__": datatypes.String("<interactive>")})
	for expr in code:
		res, namespace = execute(expr, namespace)
#		namespace["_"] = res[0]

def run_ia():
	""" interactive interpreter """
	print "Interactive interpreter:"
	namespace = init_namespace_functions({"__file__": datatypes.String("<interactive>")})
	while True:
		inp = raw_input(">>> ").strip()
		if inp == "":
			continue
		if inp == "exit":
			print "Use exit() to exit."
			continue
		if inp[0] == "!":
			if inp[1:] == "ns":
				print namespace
			elif inp[1:] == "clear":
				os.system("clear")
			else:
				print "Invalid interactive interpreter instruction."
			continue
		try:
			res, namespace = execute(parser.organise(parser.parse([inp]))[0], namespace)
		except AbortExecution, e:
			print "Error:", e
		except Exception, e:
			print "Interactive Interpreter Error:", e
			print "This is most likely bug in the interpreter."
			print "TRACING BACK:"
			raise
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
