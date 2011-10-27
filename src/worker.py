"""usage: %s [OPTS] [config-file]
Rain Worker

  -h, --help            display this message and exit
      --interface=IP    (default: localhost)
*     --port=NUM   
*     --master-addr=NUM   
*     --master-port=NUM   

note: command-line flags will override settings in the config-file
"""

import option
from urllib2 import urlopen
import time
import subprocess
import gevent_subprocess
import socket_recv
from gevent.server import StreamServer


import gevent
import subprocess
import errno
import sys
import os
import fcntl

def read_stdout (p, s):
    """Read STDOUT of process *p* non-blockingly
    Taken from gevent/examples/processes.py
    """
    fcntl.fcntl (p.stdout, fcntl.F_SETFL, os.O_NONBLOCK)

    chunks = []
    while True:
        try:
            chunk = p.stdout.read (4096)
            if not chunk:
                break
            # chunks.append (chunk)
            s.sendall (chunk)
        except IOError, ex:
            if ex[0] != errno.EAGAIN:
                raise
            sys.exc_clear ()
        gevent.socket.wait_read (p.stdout.fileno ())

    p.stdout.close ()
    # return ''.join (chunks)

def render_current (params, socket):
    args = ['echo', params]
    p = subprocess.Popen (args, stdin=None, stdout=subprocess.PIPE, \
            stderr=open ('/dev/null', 'w'))
    read_stdout (p, socket)

def handler (socket, address):
    start = time.time ()
    params = socket_recv.all (socket)
    # socket.sendall (render_current (params))
    render_current (params, socket)
    socket.close ()
    print ('%s: %0.2f ms' % (params, (time.time () - start)*1000))

def register (master_url, my_addr):
    urlopen ('%s/worker/register?ip=%s&port=%d' % ((master_url,) + my_addr))
def unregister (master_url, my_addr):
    urlopen ('%s/worker/unregister?ip=%s&port=%d' % ((master_url,) + my_addr))


if __name__ == '__main__':

    opt = option.parse (__doc__, 
            ['port=', 'interface=', 'master-url='], 
            ['port', 'master-url'], {'interface': ''})
    addr = (opt['interface'], int (opt['port']))
    master = opt['master-url']

    print 'starting worker on %s:%s' % addr
    server = StreamServer (addr, handler)
    server.pre_start ()

    register (master, addr)

    try:
        server.serve_forever ()
    except KeyboardInterrupt:
        print
    except:
        traceback.print_exc ()

    unregister (master, addr)
    print 'bye'
 
