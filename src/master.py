"""usage: %s [OPTS] config-file
Rain Master

  -h, --help            display this message and exit
  -v, --verbose         explain what is being done (XXX)
  -i, --interface       (default: localhost)
*     --port-http=NUM   
*     --port-master=NUM

note: command-line flags will override settings in the config-file
"""

import sys
import getopt
import logging
import gevent
import os.path

import wsgi_httpserver
import master_server

ARGV0 = 'master'

def parse_commandline (argv):

    def print_error (err):
        print ('%s: %s' % (ARGV0, err))
        print ("Try `%s --help' for more information." % ARGV0)

    try:
        opts, args = getopt.gnu_getopt (argv[1:], 'hi:',
                ['help', 'interface=', 'port-http=', 'port-master='])
    except getopt.GetoptError, err:
        print_error (err)
        return 2

    res = { 'interface': '' }
    if args:
        if len (args) > 1:
            print_error ('unexpected arguments (%s)' % repr (args))
            return 2

        fn = args[0]
        print ("loading configuration from '%s'" % os.path.abspath (fn))
        with open (fn) as f:
            res.update (eval ('{' + f.read () + '}'))

    for o, a in opts:
        if o in ('-h', '--help'):
            print (__doc__ % ARGV0)
            return 0
        elif o in ('-i', '--interface'):
            res['interface'] = a
        elif o in ('--port-master'):
            res['port-master'] = a
        elif o in ('--port-http'):
            res['port-http'] = a

    for mandatory in ['port-master', 'port-http']:
        if not mandatory in res:
            print_error ('--%s is a mandatory requirement' % mandatory)
            return 2

    return res


def create_logger (level=logging.INFO):
    logging.basicConfig (level=logging.INFO, stream=sys.stderr)
    return logging.getLogger (ARGV0)


if __name__ == '__main__':

    opts = parse_commandline (sys.argv)
    if isinstance (opts, int): sys.exit (opts)
    log = create_logger ()

    log.info ('hello')

    servers = [
        wsgi_httpserver.start (opts['interface'], opts['port-http'], log),
        master_server.start (opts['interface'], opts['port-master'], log)]

    try:
        gevent.event.Event ().wait ()
    except KeyboardInterrupt:
        print
        log.info ('recd KeyboardInterrupt; shutting down')

    map (lambda x: x.stop (), servers)

    log.info ('bye')


