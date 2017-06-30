'''
	Multi-thread Cache system
	LICENSE MIT @2017 Ivan LAusuch <ilausuch@gmail.com>

	Server Class. It create server socket and manages new connections
'''

import json
import logging
import random
from eventlet.green import socket
from Core.Cache import CacheItem

MAX_LEN = 4 * 1024


class Worker:
	def __init__(self, sock, address, cache):
		self.sock = sock
		self.address = address
		self.cache = cache
		self.id = random.randint(1, 1000)

	def send(self, data):
		'''
        Send a json to client
        '''
		# Convert information to json
		self.buffSend = json.dumps(data)

		# Send usign internal funcion
		self.internalSend()

	def sendData(self, data):
		'''
		Send a OK message with data
		'''
		self.send({"status": "ok", "data": data})

	def sendError(self, message):
		'''
		Send error message
		'''
		self.send({"status": "error", "message": message})

	def internalSend(self):
		'''
		Internal send message
		'''
		# Try to send message string to client
		logging.debug("Server : {0} sending {1} ".format(
			self.address, self.buffSend))

		sent = self.sock.send(str.encode(self.buffSend))

		logging.debug("Server : {0} sended {1} bytes".format(self.address, sent))

	def run(self):
		print ("Waiting...")
		line = self.sock.recv(MAX_LEN)

		while line:
			logging.debug("Received {}".format(line.strip()))

			try:
				# Try to convert to json
				op = json.loads(line.strip())
			except:
				logging.warning("Client send an invalid json")
				# TODO: Send error!
				break

			else:
				logging.info("Procesing {}".format(op))
				try:
					self.work(op)
				except socket.error as e:
					logging.info("Socket error : {}".format(e))
					self.sock.close()
					break
				except Exception as e:
					logging.error("Unexpected error : {}".format(e))
					self.sock.close()
					break
				else:
					line = self.sock.recv(MAX_LEN)

	def work(self, op):
		'''
        Executes the operation
        '''
		try:
			# Get the operation
			operation = op["op"]
		except:
			self.sendError("Operation required. Field op in json is required")
		else:
			if operation == 'put':
				self.op_put(op)
			elif operation == 'get':
				self.op_get(op)
			elif operation == 'delete':
				self.op_delete(op)
			elif operation == 'touch':
				self.op_touch(op)
			elif operation == 'getouch':
				self.op_touch(op)
			elif operation == 'bank.list':
				self.op_bankList(op)
			elif operation == 'bank.reset':
				self.op_bankReset(op)
			elif operation == 'bank.keys':
				self.op_bankKeys(op)
			else:
				self.sendError("Invalid operation")
		finally:
			logging.debug("working {} end job".format(self.id))

	def op_put(self, op):
		'''
		PUT Operation
		'''
		try:
			bank = op["bank"]
			key = op["key"]
			value = op["value"]
		except:
			self.sendError("bank, key and value are required")
		else:
			try:
				lifetime = op["lifetime"]
			except:
				lifetime = 0

			# Put the value on cache
			self.cache.put(bank, CacheItem(key, value, lifetime))

			# Send OK
			self.sendData({})

	def op_get(self, op):
		'''
		GET Operation
		'''
		try:
			bank = op["bank"]
			key = op["key"]
		except:
			self.sendError("bank and key are required")
		else:
			# Get an element from cache
			try:
				item = self.cache.get(bank, key)
			except Exception as e:
				self.sendError(str(e))
			else:
				self.sendData(item.value)

	def op_delete(self, op):
		'''
		DELETE Operation
		'''
		try:
			bank = op["bank"]
			key = op["key"]
		except:
			self.sendError("bank and key are required")
		else:
			try:
				# Remove the element
				self.cache.delete(bank, key)
			except Exception as e:
				self.sendError(str(e))
			else:
				self.sendData({})

	def op_touch(self, op):
		'''
		TOUCH Operation. Reset element timeout
		'''
		try:
			bank = op["bank"]
			key = op["key"]
		except:
			self.sendError("bank and key are required")
		else:
			try:
				self.cache.touch(bank, key)
			except Exception as e:
				self.sendError(str(e))
			else:
				self.sendData({})

	def op_getTouch(self, op):
		'''
		TOUCH Operation. Reset element timeout
		'''
		try:
			bank = op["bank"]
			key = op["key"]
		except:
			self.sendError("bank and key are required")
		else:
			try:
				item = self.cache.touch(bank, key)
			except Exception as e:
				self.sendError(str(e))
			else:
				self.sendData(item)

	def op_bankList(self, op):
		'''
		List the banks
		'''
		# If exists will return the value
		self.sendData(self.cache.getBanks())

	def op_bankReset(self, op):
		'''
		Clear a bank
		'''
		try:
			bank = op["bank"]
		except:
			self.sendError("bank are required")
		else:
			# Get the bank
			bank = self.cache.getBank(bank)

			# Reset the timeout
			bank.reset()

			# If exists will return the value
			self.sendData({})

	def op_bankKeys(self, op):
		'''
		Clear a bank
		'''
		try:
			bank = op["bank"]
		except:
			self.sendError("bank are required")
		else:
			# Get the bank
			bank = self.cache.getBank(bank)

			# If exists will return the value
			self.sendData(bank.keys())
