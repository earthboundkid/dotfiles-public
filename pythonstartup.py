#nice division, future stuff
from __future__ import division
from __future__ import unicode_literals


#Tab completion
import readline, rlcompleter
#I hate the __call__ checks!
rlcompleter.Completer._callable_postfix = lambda self, val, w: w
readline.parse_and_bind("tab: complete")


#History
import os
histfile = os.path.join(os.environ["HOME"], ".pyhist")
try:
    readline.read_history_file(histfile)
except IOError:
    pass
import atexit
atexit.register(readline.write_history_file, histfile)


#Pretty prompt
import sys
BOLD = b'\001\033[1m\002'
RESET = b'\001\033[0m\002'
sys.ps1 = BOLD + b'>>> ' + RESET
sys.ps2 = BOLD + b'... ' + RESET


#Convenience string functions
__builtins__.cat = ''.join
__builtins__.catspaces = ' '.join
__builtins__.catcommas = ', '.join
__builtins__.catlines = '\n'.join


#Nicer help
import pydoc
pydoc.pager = pydoc.plainpager


# Clean up imports
for name in list(locals()):
    if not name.startswith("_"):
        del locals()[name]
    del name
