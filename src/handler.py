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


def index (env, header):
    raise Http302 ('/static/test.html')

def worker_register (env, header):
    query = parse_qs (env.get ('QUERY_STRING', ''))
    env['rain.coordinator'].worker_register ((query['ip'][0], int (query['port'][0])))
    raise Http302 ('/worker')

def worker_unregister (env, header):
    query = parse_qs (env.get ('QUERY_STRING', ''))
    env['rain.coordinator'].worker_unregister ((query['ip'][0], int (query['port'][0])))
    raise Http302 ('/worker')

def worker (env, header):
    header['Content-Type'] = 'application/json'
    return json.dumps (env['rain.coordinator'].worker_list ())

def work (env, header):
    query = parse_qs (env.get ('QUERY_STRING', ''))
    header['Content-Type'] = 'image/png'
    print int(query['x'][0]), int(query['y'][0])
    return env['rain.coordinator'].work (int(query['x'][0]), int(query['y'][0]),int(query['lx'][0]), int(query['lz'][0]))
    return json.dumps (env['rain.coordinator'].work (int(query['x'][0]), int(query['y'][0]),int(query['lx'][0]), int(query['lz'][0])))
