#!/usr/bin/env python

import sys

def eprint(*args, **kwargs):
    if not kwargs.get('silent'): print >> sys.stderr, ' '.join(map(str, args))

