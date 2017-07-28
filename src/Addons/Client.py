'''
	Cache System Client

        Part of Multi-thread Cache system
	LICENSE MIT @2017 Ivan Lausuch <ilausuch@gmail.com>
'''

import socket
import json


class Client:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def send(self, msg):
        '''
        Send a generic message to cache system.
        It isn't recommended to use directly
        '''
        self.sock.send(msg.encode())

    def receive(self):
        '''
        Recieve a generic response from cache system.
        It isn't recommended to use directly
        '''
        return self.sock.recv(2048).decode()

    def sendOp(self, op):
        '''
        Send an operation to cache system, and wait for any response
        It isn't recommended to use directly
        '''
        self.send(op)
        return self.receive()

    def entry_set(self, bank, key, value, lifetime=0):
        '''
        Add or remplace an entry
        '''
        value = json.dumps(value)
        return self.sendOp('{"op":"put","bank":"%s","key":"%s","value":%s,"lifetime":%s}' % (bank, key, value, lifetime))

    def entry_get(self, bank, key):
        '''
        Get an entry
        '''
        return self.sendOp('{"op":"get","bank":"%s","key":"%s"}' % (bank, key))

    def entry_incr(self, bank, key, value):
        '''
        Get an entry
        '''
        return self.sendOp('{"op":"incr","bank":"%s","key":"%s","value":"%s"}' % (bank, key, value))

    def entry_delete(self, bank, key):
        '''
        Delete an entry
        '''
        return self.sendOp('{"op":"delete","bank":"%s","key":"%s"}'
                           % (bank, key))

    def entry_touch(self, bank, key):
        '''
        Update timeout of an entry
        '''
        return self.sendOp('{"op":"touch","bank":"%s","key":"%s"}'
                           % (bank, key))

    def bank_keys(self, bank):
        '''
        Get the list of entities of a bank
        '''
        return self.sendOp('{"op":"bank.keys","bank":"%s"}' % (bank))

    def bank_reset(self, bank):
        '''
        Clean all entities of a bank
        '''
        return self.sendOp('{"op":"bank.reset","bank":"%s"}' % (bank))

    def bank_list(self):
        '''
        Get the list of banks
        '''
        return self.sendOp('{"op":"bank.list"}')

    def close(self):
        self.sock.close()
