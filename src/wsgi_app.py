from mimetypes import guess_type
from wsgiref.headers import Headers
from http_exception import *
import os

import handler

STATUS_OK = '200 OK'
STATIC = '/static/'
STATIC_LOCAL = 'src'

def main (env, start_response):

    path = env['PATH_INFO']
    header = Headers ([('Content-Type', 'text/html')])

    try:
        if path.startswith (STATIC):
            status, out = serve_static (path[len (STATIC):], env, header)
        else:
            status, out = serve_dynamic (path, env, header)
    except Http302, redirect:
        status = redirect.status
        header['Content-Type'] = redirect.content_type
        header['Location'] = redirect.location
        out = redirect.out
    except HttpException, e:
        status = e.status
        header['Content-Type'] = e.content_type
        out = e.out

    if 'Content-Length' not in header:
        header['Content-Length'] = str (len (out))

    start_response (status, header.items ())
    return [out]

def serve_static (path, env, header):
    if env['REQUEST_METHOD'] != 'GET':
        raise Http404
    local_path = os.path.join (STATIC_LOCAL, path)
    try:
        f = open (local_path)
    except IOError:
        env['rain.log'].error ("file not found - '%s'", local_path)
        raise Http404
    header['Content-Type'] = guess_type (path)[0] or 'application/octet-stream'
    return STATUS_OK, f.read ()

def serve_dynamic (path, env, header):
    path = env.get ('PATH_INFO', '/')[1:]
    if not path:
        path = 'index'
    elif path == 'reload': 
        # XXX cheat code
        # hit this url to refresh stale python without restarting the server
        # maybe do this automatically using pyinotify?
        env['rain.log'].info ('reloaded handler')
        reload (handler)
        return STATUS_OK, '<em>you junkie!</em>'
    try:
        handler_fn = getattr (handler, path.replace ('/', '_'))
    except AttributeError:
        raise Http404
    return STATUS_OK, handler_fn (env, header)
