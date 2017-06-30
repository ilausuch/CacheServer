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

loggingFormat = '%(asctime)s:%(levelname)s:%(message)s'


# By default values
WORKERS = 4
SERVER_IP = "127.0.0.1"
SEVER_PORT = 10001
VERBOSE = 0

'''
Cache system
'''
cache = Cache()


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
				SERVER_IP = cfg["SERVER_IP"]
				SEVER_PORT = cfg["SERVER_PORT"]
				VERBOSE = cfg["VERBOSE"]
			except:
				print ("Required WORKERS, SERVER_IP and SERVER_PORT in config.json")
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
		logging.basicConfig(format=loggingFormat, level=logging.INFO)

	# Create server
	server = Server(cache)
	server.connect((SERVER_IP, SEVER_PORT))
	server.run()


'''
MAIN
'''
if __name__ == "__main__":
	sys.exit(main())
