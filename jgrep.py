#!/usr/bin/env python

import sys,getopt,re,json
#TODO use fileinput to provide line numbers and stdin processing,
# e.g. cat implementation
#import fileinput
#inp = fileinput.input(['rr', 'idownloader.py'])
#while True:
#    try:
#        line = inp.next()
#        print line,
#    except IOError as e:
#        print str(e)
#    except StopIteration:
#        break

def match(js, key, pattern, invert):
    match = False
    for k in filter(key.search, js.keys()):
        if pattern.search(str(js[k])): match = True
    if invert: match = not match
    return match

def all_lines(key, pattern, files, invert):
    for f in files:
        try:
            with open(f) as file:
                for lno, line in enumerate(file, start=1):
                    line = line.strip()
                    if '' == line: continue
                    try:
                        js = json.loads(line)
                        if not type(js) is dict:
                            print >> sys.stderr, 'Non dictionary at line', lno
                            continue
                        if match(js, key, pattern, invert): print line
                    except ValueError as e:
                        print >> sys.stderr, str(e), 'at line', lno
        except IOError as e:
            print >> sys.stderr, str(e)

def build_re(exp):
    try:
        regex = re.compile(exp)
    except sre_constants.error as e:
        print str(e)
        print 'In regular expression [' + exp + ']'
        sys.exit(1)
    return regex

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

# TODO
# -V, --version
# -n, --line-number
# -s, -q, --quiet, --silent, --no-messages
# -i, --ignore-case
# -I, --ignore-value-case
# -H, --with-filename
# -R, -r, --recursive

if '__main__' == __name__:
    try:
        opts,args = getopt.getopt(sys.argv[1:],"vh",["invert","help"])
    except getopt.GetoptError as e:
        print str(e)
        print usage(1)
    if 2 > len(args):
        print  usage(0)
    key     = args.pop(0)
    pattern = args.pop(0)
    invert  = False
    help    = False
    for o,a in opts:
        if   o in ('-v','--invert') : invert = True
        elif o in ('-h','--help')   : help   = True
        else : assert False, 'bad command line option'
    if help: usage(0)
    all_lines(build_re(key), build_re(pattern), args, invert)

