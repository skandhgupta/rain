import gevent

import subprocess
import errno
import sys
import os
import fcntl

def read_stdout (p):
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
            chunks.append (chunk)
        except IOError, ex:
            if ex[0] != errno.EAGAIN:
                raise
            sys.exc_clear ()
        gevent.socket.wait_read (p.stdout.fileno ())

    p.stdout.close ()
    return ''.join (chunks)
