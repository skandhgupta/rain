
# XXX
# assuming that only one greenlet at a time accesses any of the
# following functions
# fixing this might entail using
#   self.queue = gevent.queue.Queue ()
#   gevent.spawn (self.run)

import gevent
from gevent.socket import AF_INET, SOCK_STREAM, SHUT_WR
import socket_recv
from PIL import Image
import sys
import tempfile
import os

def greenlet_log_traceback (func):
    def wrapper (self, *args):
        try:
            return func (self, *args)
        except:
            self.log.exception ('greenlet failed')
            return None
    return wrapper


class Coordinator:

    def __init__ (self, log):
        self.log = log
        self.worker = []
	self.count = 0    # total number of nodes.
	self.ratio = 0    # keeps track of columns to fbe given eg, for 2 nodes ratio is 0.5

    def worker_register (self, addr):
	self.count += 1
        self.log.info ('registering worker %s count is %d', repr (addr),self. count)
        self.worker.append (addr)

    def worker_unregister (self, addr):
        self.log.info ('unregistering worker %s', repr (addr))
	self.count -= 1
        del self.worker[self.worker.index (addr)]

    def worker_list (self):
        return self.worker

    def Join (self, res):
	cnt = 0
	filename = []
	initimg = []
	tmpimg = []
	self.log.info('Total received is %s', len(res))
	for i in res:
		name = name = "lol" + str(cnt) + ".png"
		cnt += 1
		filename.append(name)
		f = open(name, "w")
		f.write(i)
		f.close()	

	for i in filename:
		initimg.append(Image.open(i))
		os.remove(i)		
	x=0
	yleft=0
	yright=initimg[0].size[1]
	totalx = initimg[0].size[0] / len(initimg)
	for i in initimg:
        	box = () 
        	box = (x, yleft, (x+totalx), yright )
        	i = i.crop(box)
        	tmpimg.append(i)
        	x += totalx
	
	ImgFile = self.Join_final(tmpimg)     
	return ImgFile
        
    def Join_final(self,res):
        w = sum(i.size[0] for i in res)
        mh = max(i.size[1] for i in res)
        result = Image.new("RGBA", (w, mh))
        x = 0
        for i in res:
                result.paste(i, (x, 0))
                x += i.size[0]
        result.save("lol.png")
	return "lol.png"

	
    def work (self, x, y, lx, lz):
	cam = ((lx*100 + lz)* 100 +x )* 100  + y
	print cam
	self.ratio = 1.0 / len(self.worker)
        jobs = [gevent.spawn (self.do_work, addr, cam, i ) for i,addr in enumerate(self.worker)]
        gevent.joinall (jobs, timeout=2)
        res = []
        for i, job in enumerate (jobs):
            try:
                v = job.get (block=False)
                if v:
                    res.append (v)
            except gevent.Timeout, t: 
                self.log.error ('worker %s timed out (%s)', self.worker[i], t)
        print 'Calling Joiner'
	#print self.count 
	#self.ratio = 1.0 / self.count
	#print self.ratio
	ImgFile = self.Join(res)
	f = open(ImgFile,"r")
	z = f.read()
	f.close()
	os.remove(ImgFile)
	return z

    	
    @greenlet_log_traceback
    def do_work (self, addr,cam,total):
	self.log.info( "worker is %s",len(self.worker))

        s = gevent.socket.socket (AF_INET, SOCK_STREAM)
        if s.connect_ex (addr) != 0:
            self.log.error ('worker %s AWOL', addr)
            self.worker_unregister (addr)
            return None
	#print 'Ratio is',self.ratio
	#si range, (range+self.ratio)
	#if (range- 1.0) >= .10:
	#	range = 0.0
	param = '+p '+'+SC'+str(total*self.ratio)+' +EC'+str(((total+1)*self.ratio))+' +K'+str(cam)
	self.log.info(param)
        s.sendall (param)
        s.shutdown (SHUT_WR)
        return socket_recv.all (s)

