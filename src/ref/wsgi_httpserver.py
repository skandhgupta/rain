"""WSGI server"""

from gevent import pywsgi as wsgi
from wsgi_app import wsgi_app

class WSGIHandler_WithCustomLogger(wsgi.WSGIHandler):

    def log_request(self):
        self.server.log.info (self.format_request())

    def log_error(self, msg, *args):
        log = self.server.log
        def gracefully_die ():
            log.error ('exception while logging error: %r %r', msg, args)
            log.error (traceback.format_exc())
        try:
            message = msg % args
        except Exception:
            gracefully_die ()
        try:
            message = '%s: %s' % (self.socket, message)
        except Exception:
            pass
        try:
            log.error (message)
        except Exception:
            gracefully_die ()

 
def start_webserver (log, interface, port):
    log.info ('Starting webserver on %s:%s', interface, port)
    gevent.pywsgi.WSGIServer((interface, port), application=wsgi_app, log=log,
            handler_class=WSGIHandler_WithCustomLogger).serve_forever()
