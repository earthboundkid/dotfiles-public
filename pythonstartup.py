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

import functools
from subprocess import Popen, PIPE

#_macrondict maps from characters with a circumflex to the corresponding
#character with a macron
_macrondict = {194: 256, 219: 362, 234: 275, 226: 257, 238: 299,
               244: 333, 206: 298, 212: 332, 251: 363, 202: 274}

def copy(s):
    "Copy string argument to clipboard"

    copy = Popen(["pbcopy"], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    _, err = copy.communicate(bytes(s, encoding="utf-8"))

    #Unlikely
    if err:
        raise Exception(err)

def paste():
    "Returns contents of clipboard"

    paste = Popen(["pbpaste"], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    b, err = paste.communicate()

    #Unlikely
    if err:
        raise Exception(err)

    return b.decode("UTF-8")

def lines(l=None):
    """Given no arguments, it returns a list of lines on the clipboard.
    Given one iterable argument, it turns everything in that into a string,
    joins them as lines and then copies that to the clipboard."""

    if l is None:
        return paste().splitlines()

    copy('\n'.join(str(i) for i in l))

def words(w=None):
    """Given no argument, it returns a list of words on the clipboard.
    Given one iterable argument, it joins them together with spaces
    and copies them to the clipboard."""
    if w is None:
        import re
        return re.split(r'\W+', paste())

    copy(' '.join(map(str, w)))


def _extend(cls):
    "Decorator to add methods to PasteBoard so it can act like a string."

    def make_method(attr):
        @functools.wraps(getattr(str, attr), ('__name__', '__doc__'))
        def wrapper(self, *args, **kwargs):
            s = paste()
            r = getattr(s, attr)(*args, **kwargs)
            return self._f(r)
        return wrapper

    attrs = ("capitalize center count encode endswith expandtabs find format "
        "format_map index isalnum isalpha isdecimal isdigit isidentifier "
        "islower isnumeric isprintable isspace istitle isupper join ljust "
        "lower lstrip maketrans partition replace rfind rindex rjust "
        "rpartition rsplit rstrip split splitlines startswith strip swapcase "
        "title translate upper zfill __gt__ __contains__ __format__ "
        "__getitem__ __len__ __mul__ __rmul__ __add__".split())

    for attr in attrs:
        setattr(cls, attr, make_method(attr))

    return cls

@_extend
class PasteBoard(object):
    def __init__(self, f):
        """PasteBoard is a decorator-class for creating convenience objects to
        interact with the clipboard in an interactive environment."""

        self._f = f

    def __str__(self):
        return paste()

    __pos__ = __str__ #Fast way to get a true string: +p

    def __iter__(self):
        return iter(paste())

    def __len__(self):
        return len(paste())

    def __repr__(self):
        return "PasteBoard({0!r})".format(paste())

    def __call__(self, s):
        copy(s)

    __truediv__ = __call__ #Fast way to copy something: p/"Text."

    def sort(self, spliton=None, key=lambda item: item.lower()):
        "Sorts the words on the pasteboard."

        r = paste()
        if spliton is not None:
            r = r.split(spliton)
        else:
            r = r.splitlines()
            spliton = "\n"
        r = spliton.join(sorted(r, key=key))
        return self._f(r)

    def ascii(self):
        return self._f(paste().encode("ascii", "ignore").decode("ascii"))

    def latin(self):
        return self._f(paste().encode("latin", "ignore").decode("latin"))

    def nonascii(self):
        return self._f(''.join(char for char in paste() if ord(char)>128))

    def indent(self):
        return self._f('\n'.join('    ' + line for line in lines()))

    def dedent(self):
        "Uses built in module textwrap to dedent."

        import textwrap
        return self._f(textwrap.dedent(paste()))

    def wrap(self, n=80):
        "Uses built in module textwrap to wraplines."

        import textwrap
        lines = paste().splitlines()
        lines = ('\n'.join(textwrap.wrap(line, n)) for line in lines)
        lines = '\n'.join(lines)
        return self._f(lines)

    def titlecase(self):
        "Not to be confused with .title(). Requires titlecase module."

        from .titlecase import titlecase
        return self._f(titlecase(paste()))

    def filename(self):
        "Strips bad characters and titlecases using titlecase module."

        from titlecase import titlecase
        s = titlecase(paste())
        s = s.replace(":", '\uff1a')
        s = s.replace("/", '\uff0f')
        s = s.replace("\n", " ")
        s = s.replace("  ", " ")
        return self._f(s)

    def eval(self):
        return eval(paste())

    def shuffle(self, split=None):
        from random import shuffle
        if split is None:
            lines = paste().splitlines()
            shuffle(lines)
            return self._f('\n'.join(lines))

        lines = paste().split(split)
        shuffle(lines)
        return self._f('\n'.join(lines))

    def formatlines(self, format_spec):
        lines = paste().splitlines()
        lines = (format_spec.format(line, line=line, index=i, i=i, n=i+1, count=i+1)
                 for i, line in enumerate(lines))
        return self._f("\n".join(lines))

    __mod__ = formatlines

    def each(self, f, split=None, joiner="\n"):
        "After splitting applies each item to function. Defaults to splitlines."

        if split is None:
            l = paste().splitlines()
        else:
            l = paste().split(split)

        return self._f(joiner.join(map(f, l)))

    def filterlines(self, f):
        lines = paste().splitlines()
        lines = filter(f, lines)
        return self._f("\n".join(lines))

    def rformat(self, s):
        return self._f(s.format(paste()))

    def __radd__(self, s):
        return self._f(s + paste())

    def transform(self, f):
        return self._f( f(paste()) )

    def macronize(self):
        "Converts text from using circumflexes to macrons."
        text = paste().translate(_macrondict)
        return self._f(text)

    def character_info(self):
        import unicodedata
        formatter = "U+{:04x} {!r}\t{}".format
        for char in paste():
            try:
                name = unicodedata.name(char)
            except ValueError:
                name = "No Name"
            print(formatter(ord(char), char, name))


@PasteBoard
def p(r):
    """p is a convenience object meant to be used in an interactive Python
    shell. p.foo() is a shortcut equivalent of paste().foo(). It returns a
    string for use in further Python functions, saving the step of first
    turning the contents of the clipboard into a string.

    Sample usage:

    >>> p
    PasteBoard('Hello, World!')
    >>> p.upper()
    'HELLO, WORLD!'
    >>> p.nonascii()
    ''
    >>> p.ascii()
    'Hello, World!'
    >>> p.rformat("Hello, '{}'!")
    "Hello, 'Hello, World!'!"
    """

    return r

@PasteBoard
def c(s):
    """c is a convenience object meant to be used in an interactive Python
    shell. c.foo() is a shortcut equivalent of copy(paste().foo()).

    Sample usage:

    >>> c("Hello, World!")
    >>> c.upper()
    Copied 'HELLO, WORLD!'.
    >>> c.lower()
    Copied 'hello, world!'.
    """

    copy(s)
    print("Copied %r." % s)

__all__ = ["copy", "paste", "lines", "words", "p", "c"]
