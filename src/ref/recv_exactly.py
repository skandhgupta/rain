"""Get an exact amount of data from a socket
http://mail.python.org/pipermail/python-dev/2010-November/105137.html
"""

ALL = ['recv_exactly']

def recv_exactly_26_or_older (socket, length):
    data = []
    while length:
        got = socket.recv (length)
        if not got:
            raise EOFError
        data.append (got)
        length -= len (got)
    return "".join (data)

def recv_exactly_27_onwards (socket, length):
    data = bytearray (length)
    view = memoryview (data)
    while length:
        got = socket.recv_into (view[-length:])
        if not got:
            raise EOFError
        length -= len (got)
    return data

try:
    memoryview (bytearray ())
    recv_exactly = recv_exactly_27_onwards 
except:
    recv_exactly = recv_exactly_26_or_older
