#!/usr/bin/env python

import sys,re,json,fileinput

def eprint(*args, **kwargs):
    if not kwargs.get('silent'): print >> sys.stderr, ' '.join(map(str, args))

def all_lines(args, params, linef, silent=False, pipe=True):
    input = fileinput.input(args)
    if pipe:  # correct behaviour over pipes, i.e. finish execution on SIGPIPE
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    while True:
        try:
            line = input.next().strip()
            if '' == line: continue
            try:
                js = json.loads(line)
                if not type(js) is dict:
                    eprint(silent, 'Non dictionary at line', lno)
                    continue
                ret = linef(js, params)
                if ret: yield ret
            except ValueError as e: eprint(silent, str(e), 'at line', lno)
        except IOError as e: eprint(silent, sys.stderr, str(e))
        except StopIteration: break

def build_re(exp, silent=False):
    regex = None
    try:
        regex = re.compile(exp)
    except re.error as e:
        eprint(str(e), 'in regular expression [' + exp + ']')
    return regex

