'''
	Multi-thread Cache system
	LICENSE MIT @2017 Ivan LAusuch <ilausuch@gmail.com>
        
        Features:
	- Unlimited entries per bank
        - Unlimited banks
        - Entries with optional lifetime
        - Number of connections only limited by system
        - Event-driven and non blocking server for minimization of CPU usage
        - Multi-thread pool of workers with deathlock protection
'''

__author__ = "ilausuch"
__date__ = "$12-jun-2017 20:14:15$"

import sys
import pyev
import json
from Queue import Queue
from Core.Server import Server
from Core.Worker import Worker
from Core.Cache import Cache

WORKERS = 4
SERVER_IP = "127.0.0.1"
SEVER_PORT = 10001


    
def main():
    
    try:
        f=file('config.json')
        data=f.read()
        
        try:
            cfg=json.loads(data)
            try:
                WORKERS = cfg["WORKERS"]
                SERVER_IP = cfg["SERVER_IP"]
                SEVER_PORT = cfg["SERVER_PORT"]
            except:
                print "Required WORKERS, SERVER_IP and SERVER_PORT in config.json"
                return
        except:
            print "config.json must be a json"
            return
    except:
        print "Requied a valid config.json file"
        return
        

    # Create job queue
    jobQueue = Queue()
    
    # Create cache
    cache = Cache()
    
    # Create workers
    workers = []
    for id in range(WORKERS):
        worker = Worker(id,jobQueue,cache)
        workers.append(worker)
        worker.start()
    
    # Create server
    server = Server(jobQueue,workers)
    server.connect((SERVER_IP,SEVER_PORT))
    server.start()
    
    # Main loop
    loop = pyev.default_loop()
    loop.start()
    

if __name__ == "__main__":
    sys.exit(main())