#!/usr/bin/env python

__version__ = '0.2'
__author__  = 'Michal Grochmal'
__licence__ = 'GNU GPL v3 or later'
__prog__    = 'jcut'
__doc__     = '''
Usage: jcut [-chrV] [-f field,field,...] [<file> ...]

  -h, --help
        print this help.

  -V, --version
        prints the version of the script.

  -f, --fields=
        comma delimited list of fields to cut from the json

  -c, --complement
        print all fields that are not in the fields list

  -r, --regex
        treat every field in the field list as a regex, this
        is useful to pattern match several similar fields or
        to match a field with a comma in it (using \\054)`
'''

import sys,getopt,json,re
import unixjso.pipe as up
import unixjso.core as uc

def cut(js, params):
    cut  = {}
    left = {}
    for k in js.keys():
        f = lambda x: x.search(k)
        if any(map(f, params['f'])) : cut[k]  = js[k]
        else                        : left[k] = js[k]
    if params.get('c'): return left
    return cut

def usage(exit):
    print __doc__
    sys.exit(exit)

if '__main__' == __name__:
    try:
        opts,args = getopt.getopt( sys.argv[1:],"hVqf:rc"
                                 , [ 'help'   , 'version' , 'quiet'
                                   , 'silent' , 'fields=' , 'regex'
                                   , 'complement'
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
        else : assert False, 'bad command line option'
    if params.get('V'):
        print __prog__, __version__
        sys.exit(0)
    if params.get('h') or not params.get('f'): usage(0)
    flds = params['f'].split(',')
    if not params.get('r'): flds = map(lambda x: '^'+re.escape(x)+'$', flds)
    params['f'] = map(lambda x: uc.build_re(x, silent=params.get('q')), flds)
    if any(map(lambda x: not x, params['f'])): sys.exit(1)
    for js in up.all_lines(args, params, cut):
        print json.dumps(js)

