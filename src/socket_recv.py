"""Extensions to Socket Receiving

Get an exact amount of data from a socket
http://mail.python.org/pipermail/python-dev/2010-November/105137.html

Get data till the peer closes his end of the pipe by calling shutdown
"""

ALL = ['exactly', 'all']

def all (socket, chunk_size=4096):
    data = []
    while True:
        got = socket.recv (chunk_size)
        if not got:
            break
        data.append (got)
    return "".join (data)

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
    exactly = recv_exactly_27_onwards 
except:
    exactly = recv_exactly_26_or_older
