#!/usr/bin/env python

__version__ = '0.3'
__author__  = 'Michal Grochmal'
__licence__ = 'GNU GPL v3 or later'
__prog__    = 'jsub'
__doc__     = '''
Usage: jsed [-hVqiI] [-f file | -e expr -e expr ...] [<file> ...]

  -h, --help
        Print this help.

  -V, --version
        Prints the version of the script.

  -q, --quiet, --silent
        Do not print anything, even on error.

  -e /pattern/replacement/, --expression=/pattern/replacement/
  -e /pattern/replacement/flags
  -e /pattern/pattern/replacement/
  -e /pattern/pattern/replacement/flags
  -e /pattern/replacement/pattern/replacement/
  -e /pattern/replacement/pattern/replacement/flags
  -e {pattern}{replacement}
  -e {pattern}{replacement}flags
  -e {pattern}{pattern}{replacement}
  -e {pattern}{pattern}{replacement}flags
  -e {pattern}{replacement}{pattern}{replacement}
  -e {pattern}{replacement}{pattern}{replacement}flags
        The substitution expression to execute, this expression
        will be run on every line on every key that matches.
        Several expressions can be specified on a single
        invocation and will be executed in the order they're
        present in the command line.  The pattern part of the
        expression is a regular expression, whilst the
        replacement part is a string that accepts '\\'
        groupings (e.g. \\1 for first grouping).

        An expression is divided into fields, each field is
        delimited by a delimiter character.  The first character
        of the expression becomes the delimiter character, every
        occurrence of that character thereof will mark the start
        of a new field.  The delimiter character must be
        printable and cannot be a digit (0-9) or one of the
        characters: 'g', 'i', '.' or '#'.  The delimiter
        character cannot be used in the fields of the
        expression.

        Also, the three grouping pairs characters '()', '[]'
        and '{}' can be used to group the fields together.
        Note that using '()' will not allow the use of grouping
        in the pattern and using '[]' will not allow the use of
        character definitions.

        Examples of equivalent expressions follows:

        Change the key 'image_id' to 'image':
            -e /image_id/image/
            -e ;image_id;image;
            -e "image_id"image"
            -e {image_id}{image}
            -e (image_id)(image)

        Every image key content from .jpg to .png
            -e /image_.*/\.jpg$/.png/g
            -e =image_.*=\.jpg$=.png=g
            -e [image_.*][\.jpg$][.png]g

        First change every field containing `image` to start
        with this word, then change every occurrence of .jpg
        to .png (note: if two fields are named `first_image`,
        `second_image` the first field will be overridden by
        the second because the substitution happens in
        ASCIIbetical order of fields).
            -e /.*image(.*)/image\\1/g -e /image.*/\.jpg/.png/g
            -e {.*image(.*)}{image\\1}g -e {image.*}{\.jpg}{.png}g
            -e /.*image(.*)/image\\1/g -e {image.*}{\.jpg}{.png}g

        More on the purpose of each field  and the `flags`
        suffix in the -e expression can be found in the
        `Expression` section, below.

  -f script_file, --file=script_file
        The script file contains one expression (as in the -e
        option) per line, which are executed in order as they
        appear in the input.  Every expression in the
        `script_file` is exactly the same as if it was passed
        to the -e flag.

        If both -f and -e are present (possibly several -e
        flags) the changes to each line of the input will
        happen by first executing the script passed by -f
        and then executing all -e flags in order.

  -i, --in-place
        Change the file in place, the default is to print the
        modified file to standard output.  If the input is
        composed of standard input only, of several files or
        of a combination of standard input and files this flag
        is ignored.

  -b extension , --backup=extension
        If -i is in effect copy the input file is copied and the
        extension `extension` is appended to it.  Only then the
        original file is modified.  If -i is in effect and -b is
        not present the changes made are irreversible.
'''

import sys,getopt,json,re
import unixjsons.pipe as up
from unixjsons.core import eprint,build_re

def sed(js, params, info=None):
    for expr in params['e']:
        peg = lambda k: expr.get(k)
        kp,kr,vp,vr,kcn,vcn = map(peg, 'kp,kr,vp,vr,kcn,vcn'.split(','))
        count = 0
        retjs = js.copy()
        for k in js:
            left = kp.search(k)
            if not left: continue
            count += 1
            if count > kcn: continue
            if kr is None: kr = left.group()  # in place
            right = kp.sub(kr, k)
            if vp:
                retjs[right] = vp.sub(vr, js[k], count=vcn)
            else:
                if right: retjs[right] = js[left.string]
                del retjs[left.string]
        js = retjs
    return retjs

def p_flags(flags):
    cnt,flg = 1,0
    if 'i' in flags:
        flg   |= re.IGNORECASE
        flags  = flags.replace('i','',1)
    if 'g' in flags:
        cnt   = 0
        flags = flags.replace('g','',1)
    elif flags.isdigit():
        cnt   = int(flags)
        flags = ''
    if flags: return [None,None]
    return [cnt,flg]

def p_expr(expr, silent=False):
    bad_delims = 'gi\\.\\#'
    splits     = { '{':'\\}\\{?' , '(':'\\)\\(?' , '[':'\\]\\[?' }
    kp,kr,vp,vr,kcn,kfl,kvl,vfl = None,None,None,None,None,None,None,None
    try:
        delim = splits.get(expr[0],re.escape(expr[0]))
        if delim in bad_delims: return None
        fields = re.split(delim,expr[1:])
    except IndexError:
        return None
    l = len(fields)
    if   3 >  l: return None
    elif 5 <  l: return None
    elif 3 == l: kp , kr ,           flags = fields
    elif 4 == l: kp ,      vp , vr , flags = fields
    elif 5 == l: kp , kr , vp , vr , flags = fields
    if   not '.' in flags and not vr: flags = flags + '.'
    elif not '.' in flags           : flags = '.' + flags
    if not 1 == flags.count('.'): return None
    kcn,kfl,vcn,vfl = reduce(list.__add__, map(p_flags, flags.split('.')))
    if any(map(lambda x: x is None, (kcn,kfl,vcn,vfl))): return None
    # /kp/kr/vp/vr/kcnkfl.vcnvfl => /kp/kr/vp/vr/kcn.vcn (kfl and vfl compiled)
    kp = build_re(kp, flags=kfl, silent=silent)
    if not vr is None: vp = build_re(vp, flags=vfl, silent=silent)
    if not kp or not vr is None and not vp: return None
    return { 'kp':kp   , 'kr':kr   , 'vp':vp   , 'vr':vr
           , 'kcn':kcn , 'kfl':kfl , 'vcn':vcn , 'vfl':vfl }

def compile(exprs, file=False, silent=False):
    comment   = re.compile(r'\s+#.*$|^#.*')
    empty     = re.compile(r'^\s*$')
    good_ones = []
    for num, expr in enumerate(exprs, 1):
        lineerr = ''
        if file:
            expr = expr.strip()
            expr = comment.sub('', expr)
            if empty.match(expr): continue
            lineerr = 'at line '+str(num)+': '
        e = p_expr(expr, silent=silent)
        if not e:
            if file: err = ''
            eprint(lineerr + 'invalid expression [' + expr +']', silent=silent)
            return None
        good_ones.append(e)
    return good_ones

def compile_script(file, silent=False):
    try:
        with open(file) as f:
            return compile(f, file=True, silent=silent)
    except IOError as e:
        eprint(str(e), silent=silent)
        return None

def usage(exit):
    print __doc__
    sys.exit(exit)

if '__main__' == __name__:
    try:
        opts,args = getopt.getopt( sys.argv[1:],'hVqf:e:iI'
                                 , [ 'help'     , 'version' , 'quiet'
                                   , 'silent'   , 'file'    , 'expression'
                                   , 'in-place' , 'backup'
                                   ])
    except getopt.GetoptError as e:
        print str(e)
        print usage(1)
    params = { 'e':[] }
    for o,a in opts:
        if   o in ('-h','--help')             : params['h']  = True
        elif o in ('-V','--version')          : params['V']  = True
        elif o in ('-q','--quiet','--silent') : params['q']  = True
        elif o in ('-f','--file')             : params['f']  = a
        elif o in ('-e','--expression')       : params['e'] += [a]
        elif o in ('-i','--in-place')         : params['i']  = True # TODO
        elif o in ('-b','--backup')           : params['b']  = a    # TODO
        else : assert False, 'bad command line option'
    if params.get('V'):
        print __prog__, __version__
        sys.exit(0)
    if params.get('h'): usage(0)
    if 1 == len(args) and 0 == len(opts): params['f'] = args.pop()
    script = []
    if params.get('f'):
        script = compile_script(params['f'], silent=params.get('q'))
        if script is None: sys.exit(1)
    exprs = compile(params['e'], silent=params.get('q'))
    if exprs is None: sys.exit(1)
    params['e'] = script + exprs
    if not params['e']: usage(0)
    for js in up.all_lines(args, params, sed):
        print json.dumps(js)

