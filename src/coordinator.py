
# XXX
# assuming that only one greenlet at a time accesses any of the
# following functions
# fixing this might entail using
#   self.queue = gevent.queue.Queue ()
#   gevent.spawn (self.run)

import gevent
from gevent.socket import AF_INET, SOCK_STREAM

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
        gevent.joinall (jobs, timeout=0.1)
        res = []
        for i, job in enumerate (jobs):
            try:
                res.append (job.get (block=False))
            except gevent.Timeout, t: 
                self.log.error ('worker %s timed out (%s)', self.worker[i], t)
        return res
        # XXX return filter (lambda x: x, [job.value for job in jobs])

    @greenlet_log_traceback
    def do_work (self, addr,token):
        s = gevent.socket.socket (AF_INET, SOCK_STREAM)
        if s.connect_ex (addr) != 0:
            self.log.error ('worker %s AWOL', addr)
            self.worker_unregister (addr)
            return None
        s.sendall ('params')
        return s.recv (10000)

