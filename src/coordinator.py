
# XXX
# assuming that only one greenlet at a time accesses any of the
# following functions
# fixing this might entail using
#   self.queue = gevent.queue.Queue ()
#   gevent.spawn (self.run)

import gevent
from gevent.socket import AF_INET, SOCK_STREAM, SHUT_WR
import socket_recv

def greenlet_log_traceback (func):
    def wrapper (self, *args):
        try:
            return func (self, *args)
        except:
            self.log.exception ('greenlet failed')
            return None
    return wrapper


class Coordinator:

    def __init__ (self, log):
        self.log = log
        self.worker = []

    def worker_register (self, addr):
        self.log.info ('registering worker %s', repr (addr))
        self.worker.append (addr)

    def worker_unregister (self, addr):
        self.log.info ('unregistering worker %s', repr (addr))
        del self.worker[self.worker.index (addr)]

    def worker_list (self):
        return self.worker

    def work (self):
        jobs = [gevent.spawn (self.do_work, addr) for addr in self.worker]
        gevent.joinall (jobs, timeout=0.9)
        res = []
        for i, job in enumerate (jobs):
            try:
                v = job.get (block=False)
                if v:
                    res.append (v)
            except gevent.Timeout, t: 
                self.log.error ('worker %s timed out (%s)', self.worker[i], t)
        return res[0]

    @greenlet_log_traceback
    def do_work (self, addr):
        s = gevent.socket.socket (AF_INET, SOCK_STREAM)
        if s.connect_ex (addr) != 0:
            self.log.error ('worker %s AWOL', addr)
            self.worker_unregister (addr)
            return None
        s.sendall ('+SC0.5')
        s.shutdown (SHUT_WR)
        return socket_recv.all (s)

