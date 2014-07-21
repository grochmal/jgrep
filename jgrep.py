#!/usr/bin/env python

__version__ = '0.7'
__author__  = 'Michal Grochmal'
__licence__ = 'GNU GPL v3 or later'
__prog__    = 'jgrep'
__doc__     = '''
Usage: jgrep [-n key] [-hVqviIHR] <key re> <value re> [<file> ...]

  -h, --help
        print this help.

  -V, --version
        prints the version of the script.

  -q, --quiet, --silent
        do not print anything, even on error

  -n key, --line-number=key
        give the line number in the output, it is added to the result under the
        key specified as the argument.

  -v, --invert-match
        print lines that do not match re pattern pattern.
'''

import sys,getopt,json,re
import unixjso.pipe as up
import unixjso.core as uc

def match(js, params, info):
    mtch = False
    for k in filter(params['key'].search, js.keys()):
        if params['pattern'].search(unicode(js[k])): mtch = True
    if params.get('v'): mtch = not mtch
    if mtch:
        if params.get('n'): return up.lineno(js, params['n'], info)
        return js
    return None

def usage(exit):
    print __doc__
    sys.exit(exit)

if '__main__' == __name__:
    try:
        opts,args = getopt.getopt( sys.argv[1:], 'hVqvn:iIHR'
                                 , [ 'help'   , 'version' , 'quiet'
                                   , 'silent' , 'invert'  , 'line-number='
                                   , 'ignore-case'   , 'ignore-value-case'
                                   , 'with-filename' , 'recursive'
                                   ])
    except getopt.GetoptError as e:
        print str(e)
        print usage(1)
    if 2 > len(args):
        print  usage(0)
    key     = uc.build_re(args.pop(0))
    pattern = uc.build_re(args.pop(0))
    if not key or not pattern: sys.exit(1)
    params  = { 'key':key , 'pattern':pattern }
    for o,a in opts:
        if   o in ('-h','--help')                  : params['h'] = True
        elif o in ('-V','--version')               : params['V'] = True
        elif o in ('-q','--quiet','--silent')      : params['q'] = True
        elif o in ('-v','--invert')                : params['v'] = True
        elif o in ('-n','--line-number')           : params['n'] = a
        elif o in ('-i','--ignore-case')           : params['i'] = True #TODO
        elif o in ('-I','--ignore-value-case')     : params['I'] = True #TODO
        elif o in ('-H','--with-filename')         : params['H'] = True #TODO
        elif o in ('-R','-r','--recursive')        : params['R'] = True #TODO
        else : assert False, 'bad command line option'
    if params.get('V'):
       print __prog__, __version__
       sys.exit(0)
    if params.get('h'): usage(0)
    for js in up.all_lines(args, params, match, silent=params.get('q')):
        print json.dumps(js)

