import sys
import getopt
import os.path

def parse (doc, flag, mandatory, res):
    """Modifies the res dictionary, and returns it too"""

    def print_error (err):
        print ('%s: %s' % (sys.argv[0], err))
        print ("Try `%s --help' for more information." % sys.argv[0])

    try:
        opt, arg = getopt.gnu_getopt (sys.argv[1:], "h", flag)
    except getopt.GetoptError, err:
        print_error (err)
        sys.exit (2)

    if arg:
        if len (arg) > 1:
            print_error ('unexpected arguments (%s)' % repr (arg))
            sys.exit (2)

        fn = arg[0]
        print ("loading configuration from '%s'" % os.path.abspath (fn))
        with open (fn) as f:
            res.update (eval ('{' + f.read () + '}'))

    for o, a in opt:
        if o in ('-h', '--help'):
            print (doc % sys.argv[0])
            sys.exit ()
        if o.startswith ('--'):
            o = o[2:]
            for f in flag:
                eq = f[-1] == '='
                if (eq and o == f[:-1]) or (not eq and o == f):
                    res[o] = a if a else True
                    break

    for m in mandatory:
        if not m in res:
            print_error ('--%s is a mandatory requirement' % m)
            sys.exit (2)
    
    return res

