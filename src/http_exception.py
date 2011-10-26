class HttpException (Exception):
    content_type = 'text/plain'
    out = ''

class Http404 (HttpException):
    status = '404 Not Found'
    out = 'Page Not Found'

class Http500 (HttpException):
    status = '500 Internal Server Error'
    out = 'Internal Server Error'

class Http302 (HttpException):
    status = '302 Found'
    def __init__ (self, location):
        self.location = location

