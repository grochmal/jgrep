#!/usr/bin/env python

import sys,re

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

