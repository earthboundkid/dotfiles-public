#nice division, future stuff
from __future__ import division
from __future__ import unicode_literals


#Tab completion
import readline, rlcompleter
#I hate the __call__ checks!
rlcompleter.Completer._callable_postfix = lambda self, val, w: w
#OS X (but not Homebrew) includes a terrible version of readline in its
#version of Python. The BSD libedit readline doesn't work with pretty
#prompt and has a different tab completion syntax.
is_bsd_readline = 'libedit' in readline.__doc__
if not is_bsd_readline:
    readline.parse_and_bind("tab: complete")
else:
    readline.parse_and_bind("bind ^I rl_complete")  # For libedit readline


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
#Only enabled if we have a *real* readline in use
if not is_bsd_readline:
    import sys
    BOLD = '\001\033[1m\002'
    RESET = '\001\033[0m\002'
    sys.ps1 = BOLD + '>>> ' + RESET
    sys.ps2 = BOLD + '... ' + RESET


#Nicer help
import pydoc
pydoc.pager = pydoc.plainpager


# Clean up imports
for name in list(locals()):
    if not name.startswith("_"):
        del locals()[name]
    del name


#Convenience string functions
cat = ''.join
catspaces = ' '.join
catcommas = ', '.join
catlines = '\n'.join
