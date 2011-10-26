"""usage: %s [OPTS] config-file
Rain Worker

  -h, --help            display this message and exit
      --interface=IP    (default: localhost)
*     --port=NUM   
*     --master-addr=NUM   
*     --master-port=NUM   

note: command-line flags will override settings in the config-file
"""

"""Simple server that listens on port 6000 and echos back every input to the client.

Connect to it with:
  telnet localhost 6000

Terminate the connection by terminating telnet (typically Ctrl-] and then 'quit').
"""
from gevent.server import StreamServer


# this handler will be run for each incoming connection in a dedicated greenlet
def echo(socket, address):
    print 'New connection from %s:%s' % address
    # using a makefile because we want to use readline()
    fileobj = socket.makefile()
    fileobj.write('Welcome to the echo server! Type quit to exit.\r\n')
    fileobj.flush()
    while True:
        line = fileobj.readline()
        if not line:
            print "client disconnected"
            break
        if line.strip().lower() == 'quit':
            print "client quit"
            break
        fileobj.write(line)
        fileobj.flush()
        print "echoed", repr(line)

def handler_create (my_addr):
    def handler (socket, address):
        socket.sendall ('server %s did connect to me %s' % (address, my_addr))
        socket.close ()
    return handler

import option
from urllib2 import urlopen

def register (master_url, my_addr):
    urlopen ('%s/worker/register?ip=%s&port=%d' % ((master_url,) + my_addr))
def unregister (master_url, my_addr):
    urlopen ('%s/worker/unregister?ip=%s&port=%d' % ((master_url,) + my_addr))

if __name__ == '__main__':

    opt = option.parse (__doc__, 
            ['port=', 'interface=', 'master-url='], 
            ['port', 'master-url'], {'interface': ''})
    addr = (opt['interface'], opt['port'])
    master = opt['master-url']

    print 'starting worker on %s:%s' % addr
    server = StreamServer (addr, handler_create (addr))
    server.pre_start ()

    register (master, addr)

    try:
        server.serve_forever ()
    except KeyboardInterrupt:
        print
    except:
        traceback.print_exc ()

    unregister (master, addr)
    print 'bye'
 
