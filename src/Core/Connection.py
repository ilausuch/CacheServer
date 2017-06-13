'''
	Multi-thread Cache system
	LICENSE MIT @2017 Ivan LAusuch <ilausuch@gmail.com>
        
        Connection class.
        Manages connection with a socket. 
        Read from socket and prepare the new jobs
'''

import time
import threading
import pyev
import socket
import logging
import signal
import weakref
import errno
import json

class Connection(object):

    def __init__(self, sock, address, loop, jobQueue, id):
        '''
        Constructor
        '''
        
        # Init
        self.sock = sock
        self.address = address
        self.sock.setblocking(0)
        self.jobQueue=jobQueue
        self.id=id
        
        self.buf = ""
        
        '''
        Add watcher to the socket
        '''
        self.watcher = pyev.Io(self.sock, pyev.EV_READ, loop, self.io_cb)
        self.watcher.start()
        
        logging.debug("{0}: ready".format(self))

    def reset(self, events):
        '''
        Restart the watcher of the socket
        '''
        self.watcher.stop()
        self.watcher.set(self.sock, events)
        self.watcher.start()

    def handle_error(self, msg):
        '''
        Force socket close
        '''
        self.close()

    def handle_read(self):
        '''
        Read new information from the socket
        '''
        try:
            # Recieve data for socket
            buf = self.sock.recv(1024)
            
        except socket.error as err:
            if err.args[0] not in NONBLOCKING:
                self.handle_error("error reading from {0}".format(self.sock))
        if buf:
            # Append to current buffer
            self.buf += buf
            
            # Reset read and write events
            self.reset(pyev.EV_READ | pyev.EV_WRITE)
            
            try:
                # Try to convert to json
                op=json.loads(self.buf)
                
                # Delete current buffer
                self.buf = ""
                
                # Add a new job to the queue
                self.jobQueue.put({"op":op,"connection":self})
            except:
                self.sendError("This is not a correct job");
        else:
            self.handle_error("connection closed by peer", logging.DEBUG, False)
    
    
    def send(self, data):
        '''
        Send a json to client
        '''
        self.buffSend = json.dumps(data)
        self.internalSend()
    
    
    def sendData(self, data):
        '''
        Send a OK message with data
        '''
        self.send({"status":"ok","data":data})
        
        
    def sendError(self, message):
        '''
        Send error message
        '''
        self.send({"status":"error","message":message})
    
    
    def internalSend(self):
        '''
        Internal send message
        '''
        try:
            #Try to send message string to client
            sent = self.sock.send(self.buffSend)
        except socket.error as err:
            if err.args[0] not in NONBLOCKING:
                self.handle_error("error writing to {0}".format(self.sock))
        else :
            self.buffSend = self.buffSend[sent:]
            if not self.buffSend:
                self.reset(pyev.EV_READ)
    

    def io_cb(self, watcher, revents):
        '''
        Socket incoming data event
        '''
        if revents & pyev.EV_READ:
            self.handle_read()

    def close(self):
        '''
        Close connection with socket and stop watchers
        '''
        self.sock.close()
        self.watcher.stop()
        self.watcher = None
        print "Closed connection"
