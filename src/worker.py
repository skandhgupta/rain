"""usage: %s [OPTS] [config-file]
Rain Worker

  -h, --help            display this message and exit
      --interface=IP    (default: localhost)
*     --port=NUM   
*     --master-addr=NUM   
*     --master-port=NUM   

note: command-line flags will override settings in the config-file
"""

import option
from urllib2 import urlopen
import traceback
import time
import povray
import socket_recv
import gevent.server


def handler (socket, address):
    start = time.time ()
    params = socket_recv.all (socket)
    povray.render_to_socket (params, socket)
    socket.close ()
    print ('%s: %0.2f ms' % (params, (time.time () - start)*1000))

def register (master_url, my_addr):
    urlopen ('%s/worker/register?ip=%s&port=%d' % ((master_url,) + my_addr))
def unregister (master_url, my_addr):
    urlopen ('%s/worker/unregister?ip=%s&port=%d' % ((master_url,) + my_addr))


if __name__ == '__main__':

    opt = option.parse (__doc__, 
            ['port=', 'interface=', 'master-url='], 
            ['port', 'master-url'], {'interface': ''})
    addr = (opt['interface'], int (opt['port']))
    master = opt['master-url']

    print 'starting worker on %s:%s' % addr
    server = gevent.server.StreamServer (addr, handler)
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
 
