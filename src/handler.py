import json
from http_exception import *

try:
    from urlparse import parse_qs
except ImportError:
    # fall back for Python 2.5
    from cgi import parse_qs


def test (env, header):
    from pprint import pprint
    from StringIO import StringIO
    out = StringIO ()
    pprint (env, stream=out)
    header['Content-Type'] = 'text/plain'
    return out.getvalue ()


count = 1
def index (env, header):
    global count
    env['rain.log'].info ('count = %d', count)
    count += 1
    import gevent
    gevent.sleep (10)
    return str (count)

def register_worker (env, header):
    query = parse_qs (env.get ('QUERY_STRING', ''))
    env['rain.coordinator'].add_worker ((query['ip'][0], int (query['port'][0])))
    raise Http302 ('/list_workers')

def list_workers (env, header):
    # XXX FOR DEBUGGING ONLY
    # header['Content-Type'] = 'application/json'
    header['Content-Type'] = 'text/plain'
    return json.dumps (env['rain.coordinator'].list_workers ())
