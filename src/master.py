"""usage: %s [OPTS] config-file
Rain Master

  -h, --help            display this message and exit
  -v, --verbose         explain what is being done (XXX)
      --interface=IP    (default: localhost)
*     --port=NUM   

note: command-line flags will override settings in the config-file
"""

import sys
import logging
import gevent

import option
import wsgi_httpserver
from coordinator import Coordinator


def create_logger (level=logging.INFO):
    logging.basicConfig (level=logging.INFO, stream=sys.stderr, 
            format='%(asctime)s %(levelname)s %(message)s')
    return logging.getLogger ()


if __name__ == '__main__':

    opt = option.parse (__doc__, ['port=', 'interface='], 
            ['port'], {'interface': ''})
    log = create_logger ()

    log.info ('hello')

    # TODO
    # pre-fork hub
    # http://groups.google.com/group/gevent/browse_thread/thread/44b756976698503b

    env = { 'rain.log' : log, 'rain.coordinator' : Coordinator (log) }
    server = wsgi_httpserver.create (opt['interface'], opt['port'], log, env)
    try:
        server.serve_forever ()
    except KeyboardInterrupt:
        print
        log.info ('recd KeyboardInterrupt; shutting down')
        server.stop ()

    log.info ('bye')


