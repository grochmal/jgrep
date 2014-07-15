#!/usr/bin/env python

__version__ = '0.1'
__author__  = 'Michal Grochmal'
__licence__ = 'GNU GPL v3 or later'
__prog__    = 'jsub'
__doc__     = '''
Usage: jsub [-hVqiI] [-f file | -e expr -e expr ...] [<file> ...]

  -h, --help
        print this help

  -V, --version
        prints the version of the script

  -q, --quiet, --silent
        do not print anything, even on error

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
        the substitution expression to execute, this expression will be run on
        every line on every key that matches.  Several expressions can be
        specified on a single invocation and will be executed in the order
        they're present in the command line.  The pattern part of the
        expression is a regular expression, whilst the replacement part is a
        string that accepts '\\\\' groupings (e.g. \\\\1 for first grouping).

        An expression is divided into fields, each field is delimited by a
        delimiter character.  The first character of the expression becomes the
        delimiter character, every occurrence of that character thereof will
        mark the start of a new field.  The delimiter character must be
        printable and cannot be a digit (0-9) or one of the characters: 'g',
        'i', '.' or '#'.  The delimiter character cannot be used in the fields
        of the expression.

        Also, the three grouping pairs characters '()', '[]' and '{}' can be
        used to group the fields together.  Note that using '()' will not allow
        the use of grouping in the pattern and using '[]' will not allow the
        use of character definitions.

        The following expressions are equivalent.

        change the key 'image_id' to 'image':
            -e /image_id/image/
            -e ;image_id;image;
            -e "image_id"image"
            -e {image_id}{image}
            -e (image_id)(image)

        every image key content from .jpg to .png
            -e /image_.*/\.jpg$/.png/g
            -e =image_.*=\.jpg$=.png=g
            -e [image_.*][\.jpg$][.png]g

        first change every field containing `image` to start with this word,
        then change every occurrence of .jpg to .png
        (note: if two fields are named `first_image`, `second_image` the first
        field will be overridden by the second as per ASCIIbetical order)
            -e /.*image(.*)/image\\\\1/g -e /image.*/\.jpg/.png/g
            -e {.*image(.*)}{image\\\\1}g -e {image.*}{\.jpg}{.png}g
            -e /.*image(.*)/image\\\\1/g -e {image.*}{\.jpg}{.png}g

        More on the purpose of each field in the -e expression can be found in
        the `Expression` section, below.

  -f script_file, --file=script_file
        the script file contains one expression (as in the -e option) per line,
        which are executed in order as they appear in the input.  Every
        expression in the `script_file`

  -i, --in-place
        change the file in place, the default is to print the modified file to
        standard output.  If the input is composed of standard input only, of
        several files or of a combination of standard input and files this flag
        is ignored.

  -b extension , --backup=extension
        if -i is in effect copy the input file is copied and the extension
        `extension` is appended to it.  Only then the original file is
        modified.  If -i is in effect and -b is not present the changes made
        are irreversible.
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

