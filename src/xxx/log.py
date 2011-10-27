"""Incomple Module -- based on stdlib code

The master receives log records from all slaves and logs them all in a 
central location. Sounds cool but is it useful?
"""

import gevent
import pickle
import struct
from recv_exactly import *

def tcp_incoming_log_record_handler_create (log):
    struct_unpacker = struct.Struct ('>L')
    def do_handle (client_socket, address):
        """Receive LogRecord and log it
        Data expected on the socket: 4 byte length + pickled LogRecord"""
        try:
            logging.getLogger (address).handle (
                    logging.makeLogRecord (
                        pickle.loads (
                            struct_unpacker.unpack (
                                recv_exactly (client_socket, 
                                    recv_exactly (client_socket, 4))))))
        except:
            log.exception ('could not log incoming record from %r', address)
    return do_handle
        
class TCPLogRecordingServer (gevent.server.StreamServer):
    """Log requests coming over TCP"""

    def __init__ (address, log, greenlet_pool):
        gevent.server.StreamServer.__init__ (
                address, 
                handle=tcp_incoming_log_record_handler_create (log), 
                spawn=greenlet_pool)

    def do_handle (self):
        """Recieve LogRecord and log it

        Data expected on the socket: 4 byte length + pickled LogRecord"""
