
# XXX
# assuming that only one greenlet at a time accesses any of the
# following functions
# fixing this might entail using
#   self.queue = gevent.queue.Queue ()
#   gevent.spawn (self.run)

class Coordinator:

    def __init__ (self, log):
        self.log = log
        self.worker = []

    def register_worker (self, addr):
        self.log.info ('adding worker %s', repr (addr))
        self.worker.append (addr)


    def list_workers (self):
        return self.worker

