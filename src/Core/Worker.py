'''
	Multi-thread Cache system
	LICENSE MIT @2017 Ivan LAusuch <ilausuch@gmail.com>
        
        Worker class. 
        Analyzes and exceutes each operation.
        It belongs to a pool of workers. All are waiting for a queue of jobs
'''

import threading
from Core.Cache import CacheItem


class Worker (threading.Thread):
    """
    Server
    """
    def __init__(self,id, jobQueue, cache):
        '''
        Initialize thread
        '''
        threading.Thread.__init__(self)
        
        #Init variables
        self.id = id
        self.jobQueue = jobQueue
        self.cache = cache
        
        self.working=True
        
        print "Worker %d : Ready" % self.id
        
    def run(self):
        '''
        Thread loop
        '''
        
        print "Worker %d : Started" % self.id
        
        while self.working:
            try:
                # Get a new job with 1 second timeout
                job = self.jobQueue.get(True,1)
                
                # Work on the job
                self.work(job)
                
                # Release the job
                self.jobQueue.task_done()
            except:
                pass
                
    def work(self,job):
        '''
        Executes the operation
        '''
        
        op = job["op"]
        connection = job["connection"]
        
        print op
        print "working %d on job" % self.id
        
        # Get the operation
        try:
            operation = op["op"]
        except:
            connection.sendError("Operation required")
            
        print "operation : %s" % op["op"]
        
        
        if operation == 'put':
            '''
            PUT Operation
            '''
            try:
                bank = op["bank"]
                key = op["key"]
                value = op["value"]
                
                try:
                    lifetime = op["lifetime"]
                except:
                    lifetime = 0
                
                # Put the value on cache
                self.cache.put(bank,CacheItem(key,value,lifetime))
                
                # Send OK
                connection.sendData({}) 
            except:
                connection.sendError("bank, key and value are required")
                
            
        elif operation == 'get':
            '''
            GET Operation
            '''
            try:
                bank = op["bank"]
                key = op["key"]
            
            except:
                connection.sendError("bank, key are required")
                
            else:
                # Get an element from cache
                item = self.cache.get(op["bank"],op["key"])
                
                if item == None:
                    # If it doesn't exist, will send error
                    connection.sendError("Invalid key")
                else:
                    # If exists will return the value
                    connection.sendData(item.value)
        else:        
            connection.sendError("Invalid operation")
        
        print "working %d end job" % self.id
        
        
    def signal_cb(self, watcher, revents):
        '''
        Error in conexion
        '''
        self.stop()
        
    def stop(self):
        '''
        Stop server
        '''
        self.working = False
        print "Worker %d : Stoped" % self.id