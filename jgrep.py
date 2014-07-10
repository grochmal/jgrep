#!/usr/bin/env python

import sys,getopt,json
import unixjs.pipe as up

def match(js, params):
    mtch = False
    for k in filter(params['key'].search, js.keys()):
        if params['pattern'].search(str(js[k])): mtch = True
    if params.get('v'): mtch = not mtch
    if mtch: return js
    return None

def usage(exit):
    print
    print 'Usage:', sys.argv[0], '[-v][-h] <key re> <value re> [<file> ...]'
    print
    print '  -h, --help'
    print '        print this help.'
    print
    #print '  -V, --version'
    print '  -v, --invert-match'
    print '        print lines that do not match re pattern pattern.'
    print
    sys.exit(exit)

if '__main__' == __name__:
    try:
        opts,args = getopt.getopt(sys.argv[1:],"vh",["invert","help"])
    except getopt.GetoptError as e:
        print str(e)
        print usage(1)
    if 2 > len(args):
        print  usage(0)
    key     = up.build_re(args.pop(0))
    pattern = up.build_re(args.pop(0))
    if not key or not pattern: sys.exit(1)
    params  = { 'key':key , 'pattern':pattern }
    for o,a in opts:
        if   o in ('-h','--help')                  : params['h'] = True
        elif o in ('-V','--version')               : params['V'] = True #TODO
        elif o in ('-v','--invert')                : params['v'] = True
        elif o in ('-n','--line-number')           : params['n'] = True #TODO
        elif o in ('-i','--ignore-case')           : params['i'] = True #TODO
        elif o in ('-I','--ignore-value-case')     : params['I'] = True #TODO
        elif o in ('-H','--with-filename')         : params['H'] = True #TODO
        elif o in ('-q','--quiet','--no-messages') : params['s'] = True #TODO
        elif o in ('-s','--silent')                : params['s'] = True #TODO
        elif o in ('-R','-r','--recursive')        : params['R'] = True #TODO
        else : assert False, 'bad command line option'
    if params.get('h'): usage(0)
    for js in up.all_lines(args, params, match):
        print json.dumps(js)

