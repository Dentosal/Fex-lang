import re
import os
import sys
import importlib



import datatypes
from meta import Token, AbortExecution, error
import corefunctions
import parser


def init_namespace_functions(namespace):
	# from corefunctions
	for function in [f for f in dir(corefunctions) if f.startswith("f_")]:
		namespace[function[2:]] = datatypes.PythonFunction(getattr(corefunctions, function))

	# from stdlib
	for file in [fn for fn in os.listdir("stdlib") if fn.endswith(".py") and not fn.startswith("_")]:
		lib = importlib.import_module("stdlib."+file.split(".")[0])
		try:
			namespace[lib.MODULE_NAME] = {}
		except AttributeError:
			error("Module 'stdlib.%s' does not define 'MODULE_NAME'" % file.split(".")[0])
		for function in [f for f in dir(lib) if f.startswith("f_")]:
			namespace[lib.MODULE_NAME][function[2:]] = datatypes.PythonFunction(getattr(lib, function))
	return namespace



def resolve_object(object_name, namespace):
	if object_name == "":
		error("Intepreter error 3: Not implemented.")
		#return datatypes.Namespace(--args--)
	ns = namespace.copy()
	for p in object_name.split("."):
		if p in ns.keys():
			ns = ns[p]
		else:
			return None
	if type(ns) == type({}):
		error("Intepreter error 3: Not implemented.")
		#return datatypes.Namespace(--args--)
	else:
		return ns


def call_function(function_name, args, namespace):
	# in-compiler functions (currently cannot be overwrited)
	if function_name == "exit":
		if len(args) == 0:
			sys.exit(0)
		elif len(args) == 1:
			if isinstance(args[0], datatypes.Integer):
				sys.exit(args[0].value)
			else:
				error("Invalid exid code type '%s'." % args[0].TYPE)
		else:
			error("exit(): invalid number of arguments: %i" % len(args))
	elif function_name == "import":
		error("Intepreter Error: Function 'import' is not implemented")


	object = resolve_object(function_name, namespace)
	if object != None:
		if isinstance(object, datatypes.Function):
			return object.call(args), namespace
		else:
			error("Cannot call non-callable type '%s'" % namespace[function_name].TYPE)

	# `function_name` not found
	error("No function_name named '%s'." % function_name)

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
		except AbortExecution, e:
			print "Error:", e
			sys.exit(1)
