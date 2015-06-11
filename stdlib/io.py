import sys

import datatypes
from meta import error, AbortExecution

def format_to_string(item):
    """ Formats value of object to printable string. """
    if isinstance(item, datatypes.String) or isinstance(item, datatypes.Integer) or isinstance(item, datatypes.Float):
        out_str = str(item.value)
    elif isinstance(item, datatypes.List):
        out_str = "[" + (", ".join([format_to_string(i) for i in item.value])) + "]"
    else:
        error("Unsupported type '%s' for '%s'" % (item.TYPE, "string_format"))
    return out_str

def f_out(args):
    """ Outputs single object without linebreak """
    if len(args) != 1:
        error("Invalid number of arguments (%s) for '%s'" % (len(args), "out"))
    out_str = format_to_string(args[0])
    sys.stdout.write(out_str)
    sys.stdout.flush()
    return args[0]
def f_print(args):
    """ Outputs line of text. If given multiple arguments, outputs them space-separated. """
    sys.stdout.write(" ".join([format_to_string(a) for a in args])+"\n")
    sys.stdout.flush()
    return args
