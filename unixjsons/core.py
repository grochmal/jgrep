#!/usr/bin/env python

import sys,re

# TODO use these two for parameter parsing
class ObjDict(dict):
    def __init__(self, **kwargs)     : self.update(kwargs)
    def __getattr__(self, name)      : return self.__getitem__(name)
    def __setattr__(self, name, val) : return self.__setitem__(name, val)
    def __delattr__(self, name)      : return self.__delitem__(name)

class ObjJsDict(dict):
    def __getattr__(self, name)      : return self.get(name)

def eprint(*args, **kwargs):
    if not kwargs.get('silent'): print >> sys.stderr, ' '.join(map(str, args))

def build_re(exp, flags=0, silent=False):
    flags = flags | re.UNICODE
    regex = None
    try:
        regex = re.compile(exp, flags)
    except re.error as e:
        eprint(str(e), 'in regular expression [' + exp + ']', silent=silent)
    return regex

