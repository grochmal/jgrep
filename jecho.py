#!/usr/bin/env python

__version__ = '0.1'
__author__  = 'Michal Grochmal'
__licence__ = 'GNU GPL v3 or later'
__prog__    = 'jecho'
__doc__     = '''
Usage: jecho [-hV] -f k:v [-f k:v -f k:v ...] [<file> ...]

  -h, --help
        Print this help.

  -V, --version
        Prints the version of the script.

  -q, --quiet, --silent
        Do not print messages.

  -f k:v, --field=k:v
        Add field `k` with value `v` to the stream.

  -r, --replace
        By default fields already in the stream will not be
        replaced, unless this flag is on.
'''

import sys,getopt,json,re
import unixjsons.pipe as up
import unixjsons.core as uc

def echo(js, pr, info):
    for k,v in pr.f:
        if not pr.r and k in js: continue
        js[k] = v
    return js

def usage(exit):
    print __doc__
    sys.exit(exit)

if '__main__' == __name__:
    try:
        opts,args = getopt.getopt( sys.argv[1:], 'hVf:r'
                                 , [ 'help'   , 'version' , 'quiet'
                                   , 'silent' , 'field='  , 'replace'
                                   ])
    except getopt.GetoptError as e:
        print str(e)
        print usage(1)
    params   = uc.ObjJsDict()
    params.f = []
    for o,a in opts:
        if   o in ('-h','--help')             : params.h  = True
        elif o in ('-V','--version')          : params.V  = True
        elif o in ('-q','--quiet','--silent') : params.q  = True
        elif o in ('-f','--fields')           : params.f += [a]
        elif o in ('-r','--replace')          : params.r  = True
        else : assert False, 'bad command line option'
    if params.V:
        print __prog__, __version__
        sys.exit(0)
    if params.h or not params.f: usage(0)
    def parse_field(f):
        if not ':' in f:
            print 'Bad field definition ['+f+']'
            return None
        return f.split(':',1)
    params.f = map(parse_field, params.f)
    for js in up.all_lines(args, params, echo):
        print json.dumps(js)

