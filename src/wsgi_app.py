def main (env, start_response):
    if env['PATH_INFO'] == '/':
        start_response('200 OK', [('Content-Type', 'text/html')])
        return ["<b>hello world</b>"]
    elif env['PATH_INFO'] == '/register':
        start_response('200 OK', [('Content-Type', 'text/html')])
        return ["<b>registered</b>"]
    else:
        start_response('404 Not Found', [('Content-Type', 'text/html')])
        return ['<h1>Not Found</h1>']
