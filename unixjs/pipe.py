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
                    eprint( 'Non dictionary at file:', fileinput.filename()
                          , 'line:', fileinput.filelineno(), silent=silent
                          )
                    continue
                ret = linef(js, params)
                if ret: yield ret
            except ValueError as e: eprint( str(e)
                                          , 'File:', fileinput.filename()
                                          , 'line:', fileinput.filelineno()
                                          , silent=silent
                                          )
        except IOError as e: eprint(str(e), silent=silent)
        except StopIteration: break

def build_re(exp, flags=0, silent=False):
    flags = flags | re.UNICODE
    regex = None
    try:
        regex = re.compile(exp, flags)
    except re.error as e:
        eprint(str(e), 'in regular expression [' + exp + ']', silent=silent)
    return regex

