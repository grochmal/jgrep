#!/usr/bin/env python

import json
from unixjsons.core import eprint

def get_dict(line, file='', line=0, silent=False):
    js = {}
    try:
        js = json.loads(ll)
        if not type(js) is dict:
            eprint( 'Non dictionary at file:', file
                  , 'line:', line, silent=silent
                  )
            js = {}
    except ValueError as e:
        eprint(str(e), 'file:', file, 'line:', line, silent=silent)
    return js

def racjoin( left, right, params, linef
           , silent=False, dropleft=False, dropright=False ):
    try:
        lfile = open(left)
        rfile = open(right)
    except IOError as e: eprint(str(e), silent=silent)
    lineno = 0
    while True:
        ll = lfile.readline()
        rl = rfile.readline()
        lineno += 1
        if not ll and not rl: break
        if dropleft  and not ll: break
        if dropright and not rl: break
        ljs = get_dict(ll, file=left,  line=lineno, silent=silent)
        rjs = get_dict(rl, file=right, line=lineno, silent=silent)
        ret = linef( ljs, rjs, params
                   , { 'l':left , 'r':right , 'line':lineno }
                   )
        if ret: yield ret

