#!/usr/bin/env python

__version__ = '0.3'
__author__  = 'Michal Grochmal'
__licence__ = 'GNU GPL v3 or later'
__prog__    = 'jcut'
__doc__     = '''
Usage: jcut [-chrlV] [-f field,field,...] [<file> ...]

  -h, --help
        Print this help.

  -V, --version
        Prints the version of the script.

  -f, --fields=
        Comma delimited list of fields to cut from the JSON.

  -c, --complement
        Print all fields that are not in the fields list.

  -r, --regex
        Treat every field in the field list as a regex, this
        is useful to pattern match several similar fields or
        to match a field with a comma in it (using \\054).

  -l, --list
        Print all available field in the input, then exit.
'''

import sys,getopt,json,re
import unixjsons.pipe as up
import unixjsons.core as uc

def cut(js, params, info=None):
    cut  = {}
    left = {}
    for k in js.keys():
        f = lambda x: x.search(k)
        if any(map(f, params['f'])) : cut[k]  = js[k]
        else                        : left[k] = js[k]
    if params.get('c'): return left
    return cut

def list_fields(js, params, info=None):
    for k in js: js[k] = 1
    return js

def usage(exit):
    print __doc__
    sys.exit(exit)

if '__main__' == __name__:
    try:
        opts,args = getopt.getopt( sys.argv[1:],"hVqf:rcl"
                                 , [ 'help'       , 'version' , 'quiet'
                                   , 'silent'     , 'fields=' , 'regex'
                                   , 'complement' , 'list'
                                   ])
    except getopt.GetoptError as e:
        print str(e)
        print usage(1)
    params = {}
    for o,a in opts:
        if   o in ('-h','--help')             : params['h'] = True
        elif o in ('-V','--version')          : params['V'] = True
        elif o in ('-q','--quiet','--silent') : params['q'] = True
        elif o in ('-f','--fields')           : params['f'] = a
        elif o in ('-r','--regex')            : params['r'] = True
        elif o in ('-c','--complement')       : params['c'] = True
        elif o in ('-l','--list')             : params['l'] = True
        else : assert False, 'bad command line option'
    if params.get('V'):
        print __prog__, __version__
        sys.exit(0)
    if params.get('h'): usage(0)
    if params.get('l'):
        fields = {}
        for js in up.all_lines(args, params, list_fields):
            for k in js:
               if not k in fields:
                   fields[k] = 1
                   print k
    elif params.get('f'):
        fs = params['f'].split(',')
        if not params.get('r'): fs = map(lambda x: '^'+re.escape(x)+'$', fs)
        params['f'] = map(lambda x: uc.build_re(x, silent=params.get('q')), fs)
        if not all(params['f']): sys.exit(1)
        for js in up.all_lines(args, params, cut):
            print json.dumps(js)
    else:
        usage(0)

