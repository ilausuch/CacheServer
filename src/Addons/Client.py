'''
	Multi-thread Cache system
	LICENSE MIT @2017 Ivan LAusuch <ilausuch@gmail.com>
        
        Client
'''

import socket
import json

class Client:
    
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host,port))
        
    def send(self,msg):
        self.sock.send(msg.encode())

    def receive(self):
        return self.sock.recv(2048).decode()

    def sendOp(self,op):
        self.send(op)
        return self.receive()
    
    def entity_put(self,bank,key,value,lifetime=0):
        value=json.dumps(value)
        return self.sendOp('{"op":"put","bank":"%s","key":"%s","value":%s,"lifetime":%s}' % (bank, key, value, lifetime))
    
    def entity_get(self,bank,key):
        return self.sendOp('{"op":"get","bank":"%s","key":"%s"}' % (bank, key))
    
    def entity_touch(self,bank,key):
        return self.sendOp('{"op":"touch","bank":"%s","key":"%s"}' % (bank, key))
    
    def bank_keys(self,bank):
        return self.sendOp('{"op":"bank.keys","bank":"%s"}' % (bank))
    
    def bank_reset(self, bank):
        return self.sendOp('{"op":"bank.reset","bank":"%s"}' % (bank))
    
    def bank_list(self):
        return self.sendOp('{"op":"bank.list"}')