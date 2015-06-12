MODULE_NAME = "io"

import sys
import datatypes
from meta import error, AbortExecution



def f_out(args):
    """ Outputs single object without linebreak """
    if len(args) != 1:
        error("Invalid number of arguments (%s) for '%s'" % (len(args), "out"))
    out_str = datatypes.format_to_string(args[0])
    sys.stdout.write(out_str)
    sys.stdout.flush()
    return args[0]
def f_print(args):
    """ Outputs line of text. If given multiple arguments, outputs them space-separated. """
    sys.stdout.write(" ".join([datatypes.format_to_string(a) for a in args])+"\n")
    sys.stdout.flush()
    return args

def f_read(args):
    """ Reads one line from stdin and returns it as string. """
    if len(args) != 0:
        error("Invalid number of arguments (%s) for '%s'" % (len(args), "read"))
    return datatypes.String(raw_input())
