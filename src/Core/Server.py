'''
	Multi-thread Cache system
	LICENSE MIT @2017 Ivan LAusuch <ilausuch@gmail.com>
        
        Server Class. It create server socket and manages new connections
'''

import time
import threading
import pyev
import socket
import signal
import weakref
import errno
import logging


from .Connection import Connection


STOPSIGNALS = (signal.SIGINT, signal.SIGTERM)
NONBLOCKING = (errno.EAGAIN, errno.EWOULDBLOCK)

class Server (threading.Thread):
    
    def __init__(self, jobQueue, workers):
        '''
        Initialize thread and other parameters
        '''
        threading.Thread.__init__(self)
        
        self.jobQueue = jobQueue
        self.workers = workers
        self.connectionCount = 0
        
        
    def connect(self, address):
        '''
        Create the server listenner
        '''
        
        #Create socket Connection and Bind
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(address)
        self.sock.setblocking(0)
        self.address = self.sock.getsockname()
        
        #Create thread loop
        self.loop = pyev.Loop()
        
        #Define watcher for signals
        self.watchers = [pyev.Signal(sig, self.loop, self.signal_cb)
                         for sig in STOPSIGNALS]
        
        #Define watcher for socket
        self.watchers.append(pyev.Io(self.sock, pyev.EV_READ, self.loop,
                                    self.io_cb))
        
        self.conns = weakref.WeakValueDictionary()
        
        logging.info("Server : Ready")
    
    def run(self):
        '''
        Thread loop
        '''
        
        # Listen 
        self.sock.listen(socket.SOMAXCONN)
        for watcher in self.watchers:
            watcher.start()
        
        logging.info("Server : Started")
        
        # Start event loop
        self.loop.start()
            
    def handle_error(self, msg):
        '''
        If there is some error, it will finish
        '''
        self.stop()

    def signal_cb(self, watcher, revents):
        '''
        Error in conexion
        '''
        self.stop()

    def io_cb(self, watcher, revents):
        '''
        When there is a new connection
        '''
        try:
            while True:
                try:
                    # Accept connection
                    sock, address = self.sock.accept()
                except socket.error as err:
                    if err.args[0] in NONBLOCKING:
                        break
                    else:
                        raise
                else:
                    logging.debug("Server : {0} New connection".format(address))
                    
                    # Create a new connection
                    self.conns[address] = Connection(sock, address, 
                        self.loop, 
                        self.jobQueue, 
                        self.connectionCount)
                    
                    # Increase connection counter
                    self.connectionCount=self.connectionCount+1

                    
        except Exception:
            self.handle_error("error accepting a connection")


    def stop(self):
        '''
        Stop server
        '''
        self.loop.stop(pyev.EVBREAK_ALL)
        
        # Socket stop
        self.sock.close()
        
        # Stop all watchers
        while self.watchers:
            self.watchers.pop().stop()
        
        for conn in self.conns.values():
            conn.close()
            
        # Call for stop all workers
        for worker in self.workers:
            worker.stop()
        
        logging.info("Server : Stoped")
            