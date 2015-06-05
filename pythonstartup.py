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
sys.ps1 = b'\001\033[1m\002>>> \001\033[0m\002'
sys.ps2 = b'\001\033[1m\002... \001\033[0m\002'


#Convenience string functions
cat = ''.join
catspaces = ' '.join
catcommas = ', '.join
catlines = '\n'.join


#Nicer help
import pydoc
pydoc.pager = pydoc.plainpager
