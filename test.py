# test that everything that has worked before still works

import sys
import subprocess as sp

TESTS = [   # format:  [["<file>", "<output>", "<input=''>"], ...]
    ["io.fex", "[42, 3.14, \"Hello World!\"]Test\n[42, 3.14, \"Hello World!\"] 1 2.5 Hello\n", "Test\n"],
]

for t in TESTS:
    p = sp.Popen(["python", "interpreter.py", "/".join(["tests", t[0]])], stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.PIPE)
    out = p.communicate(input=(t[2] if len(t)==3 else ""))
    if out != (t[1], ""): # not (stdout == t[1], stderr == "")
        print "Error in test:", t[0]
        print "STDIN:  '%s'" % (t[2] if len(t)==2 else "")
        print "STDOUT: '%s'" % out[0]
        print "STDERR: '%s'" % out[1]
        sys.exit(0)

print "Tests ok."
