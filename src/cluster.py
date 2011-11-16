# This file is meant to be run without calling 'source activate', and hence
# must not use any virtualenv specific modules

from glob import glob
import os
from signal import SIGTERM
import multiprocessing
import subprocess
import re
import socket
import random
import fcntl
import struct


#XXX
NO_PROXY_HACK="http_proxy=''"
#NO_PROXY_HACK=""

PIDF_DIR = 'ven/var/run/'
LOGF_DIR = 'ven/var/run/'

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def my_public_ip ():
    	#return get_ip_address('eth0')
	return filter (lambda ip: not ip.startswith ('127.'), 
            socket.gethostbyname_ex (socket.gethostname ())[2])[0]

def local_stop_workers ():
    for f in glob (os.path.join (PIDF_DIR, 'worker-*.pid')):
        background_kill (f)
        os.remove (f)

def local_start_workers (master_url):
    nw = multiprocessing.cpu_count ()
    public_ip = my_public_ip ()
    for port in random.sample (range (2000, 4000), nw):
        cmd = ['python', 'src/worker.py', '--master-url', master_url,
                '--interface', public_ip, '--port', str (port)]
        cmd = ' '.join (cmd)
        pidf = os.path.join (PIDF_DIR, 'worker-%s.pid' % port)
        background_spawn (pidf, '/dev/null', cmd)
    

def background_spawn (pidf, logf, cmd):
    # python-daemon is a pain, and nohup + subprocess == no pid, so ...
    cmdline = """
    /sbin/start-stop-daemon --start --pidfile %s
        --background --make-pidfile
        --exec /bin/bash -- -c 'cd %s && source activate && exec %s 2>>%s'
        """ % (pidf, os.path.abspath (os.curdir), cmd, logf)
    cmdline = re.sub (r'\s+', ' ', cmdline)
    subprocess.check_call (cmdline, shell=True)

def background_kill (pidf):
    subprocess.check_call (["start-stop-daemon", "--stop", 
        "--oknodo", "--pidfile", pidf])


def start_master (ip, port):
    cmd = ['python', 'src/master.py', '--interface', ip, '--port', str (port)]
    cmd = ' '.join (cmd)
    pidf = os.path.join (PIDF_DIR, 'master.pid')
    logf = os.path.join (LOGF_DIR, 'master.log')
    background_spawn (pidf, logf, cmd)
    
def stop_master ():
    pidf = os.path.join (PIDF_DIR, 'master.pid')
    background_kill (pidf)
    os.remove (pidf)


def remote_do (opt, command, arg):
    for worker in opt['workers']:
        subprocess.check_call (['ssh', worker, '/bin/bash', 
            '-c', "'cd %s && %s python %s --worker %s %s'" % (opt['remote-dir'],
                NO_PROXY_HACK, 'src/cluster.py', command, arg)])
 

def remote_start_all_workers (opt):
    remote_do (opt, '--start', 
            'http://%s:%d' % (opt['master']['ip'], opt['master']['port']))

def remote_stop_all_workers (opt):
    remote_do (opt, '--stop', '')

def remote_update_all_workers (opt):
    for worker in opt['workers']:
        subprocess.check_call (['scp', opt['povray-ini'], 
            '%s:%s' % (worker, 
                os.path.join (opt['remote-dir'], opt['povray-ini']))])


def load_dict (fname):
    with open (fname) as f:
        return eval ('{' + f.read () + '}')
    

if __name__ == '__main__':
    import sys
    if sys.argv[1] in ('-h', '--help'):
        print 'usage: %s <config-file> --start|stop|update' % sys.argv[0]
        sys.exit ()

    if sys.argv[2] == '--start':
        if sys.argv[1] == '--worker':
            local_start_workers (sys.argv[3])
        else:
            opt = load_dict (sys.argv[1])
            start_master (opt['master']['ip'], opt['master']['port'])
            remote_start_all_workers (opt)
    elif sys.argv[2] == '--stop':
        if sys.argv[1] == '--worker':
            local_stop_workers ()
        else:
            opt = load_dict (sys.argv[1])
            remote_stop_all_workers (opt)
            stop_master ()
    elif sys.argv[2] == '--update':
        remote_update_all_workers (load_dict (sys.argv[1]))
