#!/usr/bin/env python

__version__ = '0.1'
__author__  = 'Michal Grochmal'
__licence__ = 'GNU GPL v3 or later'
__prog__    = 'jsed'
__doc__     = '''
Usage: jsed [-hVqiI] [-f file | -e expr -e expr ...] [<file> ...]

  -h, --help
        print this help.

  -V, --version
        prints the version of the script.

  -q, --quiet, --silent
        do not print anything, even on error

  -f, --file

  -e, --expression

  -i, --in-place

  -I, --inline
'''

import sys,getopt,json,re
import unixjs.pipe as up

def sed(js, params):
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
        opts,args = getopt.getopt( sys.argv[1:],"hVqf:e:iI"
                                 , [ 'help'     , 'version' , 'quiet'
                                   , 'silent'   , 'file'    , 'expression'
                                   , 'in-place' , 'inline'
                                   ])
    except getopt.GetoptError as e:
        print str(e)
        print usage(1)
    params = {}
    for o,a in opts:
        if   o in ('-h','--help')             : params['h'] = True
        elif o in ('-V','--version')          : params['V'] = True
        elif o in ('-q','--quiet','--silent') : params['q'] = True
        elif o in ('-f','--file')             : params['f'] = a
        elif o in ('-e','--expression')       : params['e'] = True
        elif o in ('-i','--in-place')         : params['i'] = True
        elif o in ('-I','--inline')           : params['I'] = True
        else : assert False, 'bad command line option'
    if params.get('V'):
        print __prog__, __version__
        sys.exit(0)
    if params.get('h') or not params.get('f'): usage(0)
    flds = params['f'].split(',')
    if not params.get('r'): flds = map(lambda x: '^'+re.escape(x)+'$', flds)
    params['f'] = map(lambda x: up.build_re(x, silent=params.get('q')), flds)
    if any(map(lambda x: not x, params['f'])): sys.exit(1)
    for js in up.all_lines(args, params, cut):
        print json.dumps(js)

