#!/usr/bin/env python

import json,fileinput
from unixjso.core import eprint

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
                info = { 'file' : fileinput.filename()
                       , 'line' : fileinput.filelineno()
                       }
                js = json.loads(line)
                if not type(js) is dict:
                    eprint( 'Non dictionary at file:', info['file']
                          , 'line:', info['line'], silent=silent
                          )
                    continue
                ret = linef(js, params)
                if ret: yield ret
            except ValueError as e: eprint( str(e)
                                          , 'file:', info['file']
                                          , 'line:', info['line']
                                          , silent=silent
                                          )
        except IOError as e: eprint(str(e), silent=silent)
        except StopIteration: break

