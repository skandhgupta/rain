"""usage: %s [OPTS] [master|slave]
Rain

  -h, --help            display this message and exit
  -v, --verbose         explain what is being done
  -i, --interface       (default: localhost)
* -p, --port=NUM       
  -x, --validate        enable validation of the wsgi application
  -d, --daemon          daemonize the server (default: the application
                        runs in the foreground and prints a copy of its
                        log on the stdout)
  -D, --directory=PATH  the root directory of the website (default: .)
"""

def create_logger (level, sink):
    log = logging.getLogger (__name__)
    log.setLevel (level)
    def log_null (*args, **kw):
        pass
    def log_stream (msg, *args, **kwargs):
        stream.write (msg % args)
        if not kwargs.get ('continued', False):
            stream.write ('\n')
        stream.flush ()
    return log_stream if enabled else log_null

def kick_user (err):
    print ('configure: %s' % err)
    print ("Try `%s --help' for more information." % sys.argv[0])
    sys.exit (2)

def generate_help (features):
    out = StringIO ()
    for f in features:
        out.write ('  %s\t\t%s [%s]\n' % f)
    return out.getvalue ()

fval = {}
for f in features:
    fval[f[0]] = f[2]

try:
    opts, args = getopt.getopt (sys.argv[1:], 'qh',
            ['quiet', 'help'] \
                    + fval.keys () \
                    + ['no-'+f for f in fval.keys ()])
except getopt.GetoptError, err:
    kick_user (err)

if args:
    kick_user ('unexpected arguments (%s)' % repr (args))

quiet = False

for o, a in opts:
    if o in ('-h', '--help'):
        print (__doc__ % generate_help (features))
        sys.exit ()
    elif o in ('-q', '--quiet'):
        quiet = True
    else:
        if o.startswith ('--no-'):
            f = o[5:]
            e = False
        else:
            f = o[2:]
            e = True
        fval[f] = e

log = create_logger (not quiet, sys.stdout)
out = StringIO () 

for f, e in fval.items ():
    log ('Configuring %s... ', f, continued=True)
    try:
        e = globals ()[f.replace ('-', '_')] (e, out, log)
    except:
        sys.exit ()
    log ('enabled' if e else 'disabled')

log ('Writing configuration to Makefile... ', continued=True)
with open ('.Makefile.config', 'w') as f:
    f.write (out.getvalue ())
log ('done')
from syslog import *
import sys
import getopt
import os
import daemon
from daemon.pidfile import TimeoutPIDLockFile
import traceback
import lockfile

import wsgi_main

if __name__ == "__main__":
    argv0 = 'minione'
    def die_of_bad_input (err):
        print '%s: %s' % (argv0, err)
        print "Try `%s --help' for more information." % (argv0,)
        sys.exit (2)

    try:
        opts, args = getopt.getopt (sys.argv[1:], 'hvxdi:p:D:',
                ['help', 'verbose', 'validate', 'daemon', 'interface=', 
                    'port=', 'directory='])
    except getopt.GetOptError, err:
        die_of_bad_input (str (err))

    interface = ''
    port = None
    log_level = LOG_NOTICE
    validate, daemonize = False, False
    directory = '.'
    for o, a in opts:
        if o in ('-h', '--help'):
            print __doc__ % (argv0,)
            sys.exit ()
        elif o in ('-v', '--verbose'):
            log_level = LOG_DEBUG
        elif o in ('-x', '--validate'):
            validate = True
        elif o in ('-d', '--daemon'):
            daemonize = True
        elif o in ('-i', '--interface'):
            interface = a
        elif o in ('-p', '--port'):
            try:
                port = int (a)
            except ValueError:
                die_of_bad_input ("invalid port number '%s'" % port)
        elif o in ('-D', '--directory'):
            directory = a

    if not port:
        die_of_bad_input ('you must specify a port number')

    sl_flags = 0
    if not daemonize:
        sl_flags = LOG_PERROR
    openlog (argv0, sl_flags, LOG_USER)
    setlogmask (LOG_UPTO (log_level))

    # XXX
    pidfile = os.path.abspath (os.path.join (
        os.curdir, 'var', 'run', '%s.pid' % (argv0)))
    sys.path.append (os.path.dirname (os.path.abspath (__file__)))
    import wsgi_app

    syslog (LOG_DEBUG, "changing directory to '%s'" % (directory,))
    os.chdir (directory)
    syslog (LOG_DEBUG, "root directory is '%s'" % os.path.abspath (os.curdir))

    def do_main ():
        wsgi_main.start_server ('wsgi_app', interface, port, validate=validate)

    try:
        if daemonize:
            # XXX DAEMON MODE IS NOT PROPERLY FUNCTIONAL
            print 'starting %s in daemon mode - use kill '\
                    '`cat %s` to exit' % (argv0, pidfile,)
            context = daemon.DaemonContext (working_directory=os.curdir,
                    pidfile=TimeoutPIDLockFile (pidfile, 1))
            try:
                with context:
                    try:
                        do_main ()
                    except SystemExit:
                        # XXX FIXME:
                        # sigterm does not seem to work the first time around
                        context.close ()
            except lockfile.LockTimeout:
                # FIXME: report on stdout?
                syslog ('an instance is already running')
                # XXX sys.exit ()
        else:
            try:
                print 'starting %s in foreground mode - '\
                        'press ^C to exit' % (argv0,)
                do_main ()
            except KeyboardInterrupt:
                print ''
    except:
        for line in traceback.format_exception (*sys.exc_info ()):
            syslog (LOG_DEBUG, line)

    # FIXME: proper cleanup
    syslog ('exiting')
    closelog ()
