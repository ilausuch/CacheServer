#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "ilausuch"
__date__ = "$16-jun-2017 22:31:10$"

import sys
import json

from flask import Flask
from flask import request
from flask import make_response
from flask_cors import CORS

from Addons.Client import Client

from APICore.Entity import Entity
from APICore.Bank import Bank
from APICore.Cache import Cache

SERVER_IP = "127.0.0.1"
SEVER_PORT = 10001

'''
Load configuration
'''
try:
    f=open('config.json')
    data=f.read()

    try:
        cfg=json.loads(data)
        try:
            SERVER_IP = cfg["SERVER_IP"]
            SEVER_PORT = cfg["SERVER_PORT"]
        except:
            print ("Required SERVER_IP and SERVER_PORT in config.json")
            sys.exit(1)
    except:
        print ("config.json must be a json")
        sys.exit(1)
except:
    print ("Requies the config.json file")
    sys.exit(1)

'''
Create a client
'''
client=Client(SERVER_IP,SEVER_PORT)

def sendJson(data):
    resp = make_response(data)
    resp.headers['Content-Type'] = "application/json"
    return resp
    
'''
API
'''
# Start flask application
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Cache system API"

'''
Entries operations
'''

@app.route('/bank/<bank>/entry/<key>',methods=['GET', 'POST','PUT'])
def entry(bank,key):
    
    if request.method == 'POST':
        '''
        Set a entry
        '''
        return sendJson(Entity(client, bank, key).post(request.data.decode()))
    
    elif request.method == 'PUT':
        '''
        Modification of a entry
        '''
        return sendJson(Entity(client, bank, key).put(requerst))
    
    else:
        '''
        Get entry value
        '''
        return sendJson(Entity(client, bank, key).get())
    
@app.route('/bank/<bank>/entries',methods=['GET'])
def entries(bank):
    '''
    Get entries of a bank
    '''
    return sendJson(Bank(client, bank).getKeys())

@app.route('/bank/<bank>',methods=['PUT'])
def bank(bank):
    if request.method == 'PUT':
        '''
        Modification of a Bank
        '''
        return sendJson(Bank(client, bank).put(request))

@app.route('/banks',methods=['GET'])
def banks():
    '''
    Get all banks
    '''
    return sendJson(Cache(client).getBanks())


if __name__ == "__main__":
    app.run(debug=True)
    
