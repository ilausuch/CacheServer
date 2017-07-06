#! /usr/bin/python
'''
    Restful API for Multi-thread Cache system
    LICENSE MIT @2017 Ivan LAusuch <ilausuch@gmail.com>
'''

__author__ = "ilausuch"
__date__ = "$16-jun-2017 22:31:10$"

import sys
import json
import falcon
import logging

from falcon_cors import CORS

from Addons.Client import Client

from APICore.Entity import Entity
from APICore.Bank import Bank
from APICore.Cache import Cache

logging.basicConfig(level=logging.DEBUG)

# By default values
SERVER_IP = "127.0.0.1"
SEVER_PORT = 10001

'''
Load configuration
'''
try:
    f = open('config.json')
    data = f.read()

    try:
        cfg = json.loads(data)
        try:
            SERVER_IP = cfg["CACHE_SERVER_IP"]
            SEVER_PORT = cfg["CACHE_SERVER_PORT"]
            API_PATH = cfg["API_PATH"]

        except:
            print ("Required CACHE_SERVER_IP, CACHE_SERVER_PORT API_PATH in config.json")
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
client = Client(SERVER_IP, SEVER_PORT)

'''
API
'''


def sendJson(resp, data):
    # resp.headers['Content-Type'] = "application/json"
    resp.body = json.dumps(data)


class index:
    def on_get(self, req, resp):
        resp.body = "Cache system API"


class entry:
    def on_get(self, req, resp, **params):
        try:
            bank = params["bank"]
            key = params["key"]
        except Exception:
            raise falcon.HTTPBadRequest('Invalid request',
                                        "bank and key are required parameters")

        try:
            result = Entity(client, bank, key).get()
            js = json.loads(result)
        except Exception:
            raise falcon.HTTPServiceUnavailable('Service Outage',
                                                'Internal error', 30)
        else:
            if js["status"] == 'error':
                raise falcon.HTTPBadRequest('Cache Server error message',
                                            js["message"])

            sendJson(resp, js)

    def on_post(self, req, resp, **params):
        try:
            bank = params["bank"]
            key = params["key"]
        except Exception:
            raise falcon.HTTPBadRequest('Invalid request',
                                        "bank and key are required parameters")

        try:
            result = Entity(client, bank, key).post(req.stream.read())
            js = json.loads(result)
        except Exception:
            raise falcon.HTTPServiceUnavailable('Service Outage',
                                                'Internal error', 30)
        else:
            if js["status"] == 'error':
                raise falcon.HTTPBadRequest('Cache Server error message',
                                            js["message"])

            sendJson(resp, js)


class entries:
    def on_get(self, req, resp, **params):
        try:
            bank = params["bank"]
        except Exception:
            raise falcon.HTTPBadRequest('Invalid request',
                                        "bank is a required parameters")

        try:
            result = Bank(client, bank).getKeys()
            js = json.loads(result)
        except Exception:
            raise falcon.HTTPServiceUnavailable('Service Outage',
                                                'Internal error', 30)
        else:
            if js["status"] == 'error':
                raise falcon.HTTPBadRequest('Cache Server error message',
                                            js["message"])

            sendJson(resp, js)


class bank:
    def on_put(self, req, resp, **params):

        try:
            bank = params["bank"]
        except Exception:
            raise falcon.HTTPBadRequest('Invalid request',
                                        "bank is a required parameters")

        try:
            result = Bank(client, bank).put(req.params)
            js = json.loads(result)
        except Exception:
            raise falcon.HTTPServiceUnavailable('Service Outage',
                                                'Internal error', 30)
        else:
            if js["status"] == 'error':
                raise falcon.HTTPBadRequest('Cache Server error message',
                                            js["message"])

            sendJson(resp, js)


class banks:
    def on_get(self, req, resp, **params):
        try:
            result = Cache(client).getBanks()
            js = json.loads(result)
        except Exception:
            raise falcon.HTTPServiceUnavailable('Service Outage',
                                                'Internal error', 30)
        else:
            if js["status"] == 'error':
                raise falcon.HTTPBadRequest('Cache Server error message',
                                            js["message"])

            sendJson(resp, js)


cors = CORS(allow_all_origins=True, allow_all_headers=True,
            allow_methods_list=['GET', 'POST', 'PUT', 'OPTIONS'])

api = falcon.API(middleware=[cors.middleware])

api.add_route(API_PATH + '/', index())
api.add_route(API_PATH + '/bank/{bank}/entry/{key}', entry())
api.add_route(API_PATH + '/bank/{bank}/entries', entries())
api.add_route(API_PATH + '/bank/{bank}', bank())
api.add_route(API_PATH + '/banks', banks())
