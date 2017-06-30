'''
	Multi-thread Cache system
	LICENSE MIT @2017 Ivan LAusuch <ilausuch@gmail.com>

	Server Class. It create server socket and manages new connections
'''

import logging

import eventlet
from Core.Worker import Worker


class Server ():

	def __init__(self, cache):
		'''
		Initialize
		'''
		self.cache = cache

	def connect(self, address):
		'''
		Create the server listenner
		'''

		# Create socket Connection and Bind
		self.ssock = eventlet.listen(address)

		logging.info("Server : Ready")

	def run(self):
		'''
		Thread loop
		'''
		try:
			while True:
				sock, address = self.ssock.accept()

				logging.info("Server - New connection from {}".format(address))

				eventlet.spawn_n(self.work, address, sock)

		except (KeyboardInterrupt, SystemExit):
			print("Server - Exit")

	def work(self, address, sock):
		'''
		Executes the worker
		'''
		worker = Worker(sock, address, self.cache)
		worker.run()

	def stop(self):
		'''
		Stop server
		'''

		# Socket stop
		self.ssock.close()

		# Call for stop all workers
		for worker in self.workers:
			worker.stop()

		logging.info("Server : Stoped")
