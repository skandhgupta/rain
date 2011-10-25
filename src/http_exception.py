class HttpException (Exception):
    content_type = 'text/plain'

class Http404 (HttpException):
    status = '404 Not Found'
    out = 'Page Not Found'

class Http500 (HttpException):
    status = '500 Internal Server Error'
    out = 'Internal Server Error'
    content_type = 'text/plain'

class Http302 (HttpException):
    status = '302 Found'
    out = ''
    def __init__ (self, location):
        self.location = location

