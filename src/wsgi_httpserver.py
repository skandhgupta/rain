"""WSGI HTTP server"""

from gevent import pywsgi as wsgi
import wsgi_app

class WSGIHandler_WithCustomLogger(wsgi.WSGIHandler):

    def log_request(self):
        self.server.log.info (self.format_request ())

    def log_error(self, msg, *args):
        log = self.server.log

        def log_traceback ():
            log.error ('exception while logging error: %r %r', msg, args)
            log.error (traceback.format_exc ())

        try:
            message = msg % args
        except Exception:
            log_traceback ()
        try:
            message = '%s: %s' % (self.socket, message)
        except Exception:
            pass
        try:
            log.error (message)
        except Exception:
            log_traceback ()

 
def create (interface, port, log):
    log.info ('starting webserver on %s:%s', interface, port)
    server = wsgi.WSGIServer ((interface, int (port)), 
            application=wsgi_app.main, 
            log=log, handler_class=WSGIHandler_WithCustomLogger)
    return server
