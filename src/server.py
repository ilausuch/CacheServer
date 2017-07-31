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
import json
import logging

try:
    from queue import Queue  # For python 3
except:
    from Queue import Queue  # For python 2

from Core.Server import Server
from Core.Cache import Cache
from Core.UpdaterServer import UpdaterServer
from Core.UpdaterWorker import UpdaterWorker

loggingFormat = '%(asctime)s:%(levelname)s:%(message)s'

# Context
context = {
    "cache": Cache(),
    "updatingQueue": Queue(),
    "updatingConnections": []
}


def main():
    '''
    MAIN
    '''
    try:
        f = open('config.json')
        data = f.read()

        try:
            cfg = json.loads(data)
            try:
                SERVER_IP = cfg["CACHE_SERVER_IP"]
                SEVER_PORT = cfg["CACHE_SERVER_PORT"]
                CACHE_SERVER_LISTENNER_PORT = cfg["CACHE_SERVER_LISTENNER_PORT"]
                VERBOSE = cfg["CACHE_VERBOSE"]
            except:
                print ("Required WORKERS, SERVER_IP, SERVER_PORT, CACHE_SERVER_LISTENNER_PORT in config.json")
                return
        except:
            print ("config.json must be a json")
            return
    except:
        print ("Requies the config.json file")
        return

    if VERBOSE:
        logging.basicConfig(format=loggingFormat, level=logging.DEBUG)
    else:
        logging.basicConfig(format=loggingFormat, level=logging.WARNING)

    # Create updater server
    updaterServer = UpdaterServer(context)
    updaterServer.connect((SERVER_IP, CACHE_SERVER_LISTENNER_PORT))
    updaterServer.start()

    # Create updater worker
    updaterWorker = UpdaterWorker(context)
    updaterWorker.start()

    # Create server
    server = Server(context)
    server.connect((SERVER_IP, SEVER_PORT))
    server.run()


'''
MAIN
'''
if __name__ == "__main__":
    sys.exit(main())
