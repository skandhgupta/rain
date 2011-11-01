import gevent

import subprocess
import errno
import sys
import os
import fcntl

def pipe_stdout_to_socket (p, s):
    """Pipe stdout of process to socket non-blockingly
    Modification of gevent/examples/processes.py
    """
    fcntl.fcntl (p.stdout, fcntl.F_SETFL, os.O_NONBLOCK)

    chunks = []
    while True:
        try:
            chunk = p.stdout.read (4096)
            if not chunk:
                break
            s.sendall (chunk)
        except IOError, ex:
            if ex[0] != errno.EAGAIN:
                raise
            sys.exc_clear ()
        gevent.socket.wait_read (p.stdout.fileno ())

    p.stdout.close ()

def render_to_socket (params, socket):
    args = ['povray', 'etc/povray.ini'] + params.split ()
    p = subprocess.Popen (args, stdin=None, stdout=subprocess.PIPE, \
            stderr=open ('/dev/null', 'w'))
    pipe_stdout_to_socket (p, socket)
