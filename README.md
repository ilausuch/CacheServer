# CacheServer

Multi-thread Cache system based on Banks of entities. A bank is a group of entities.

## License

LICENSE MIT @2017 Ivan Lausuch <ilausuch@gmail.com>

## Features

* Unlimited entries per bank
* Unlimited banks
* Entries with optional lifetime
* Number of connections only limited by system
* Event-driven and non blocking server for minimization of CPU usage
* Multi-thread pool of workers with death-lock protection

## Server

### Configuration file

A config.json file is required. It must include:

* WORKERS : Number of workers to process operations
* SERVER_IP : IP of the server
* SERVER_PORT : Port of the server

Example:

    {
        "WORKERS" : 4,
        "SERVER_IP" : "127.0.0.1",
        "SERVER_PORT" : 10001
    }

### Execution

To execute use this:

    python main.py

On console will appear the initialization

    Worker 0 : Ready
    Worker 0 : Started
    Worker 1 : Ready
    Worker 1 : Started
    Worker 2 : Ready
    Worker 2 : Started
    Worker 3 : Ready
    Worker 3 : Started
    Server : Ready
    Server : Started



## Client

To connect to server only is required a socket connection. 
In fact any language can be used. Next example has been written in python

    import socket
    import time

    def send(sock, msg):
        sock.send(msg)

    def receive(sock):
        return sock.recv(2048)

    def sendOp(sock,op):
        send(sock,op)
        return receive(sock)

    def main():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 10001))

        print sendOp(sock,'{"op":"put","bank":"1","key":"test1","value":"test1v","lifetime":1}')
        print sendOp(sock,'{"op":"get","bank":"1","key":"test1"}')
        
    if __name__ == "__main__":
        main()



## API

To perform operations is required send a valid JSON with the operation parameters.
And client will receive a JSON as response

If operation has been executed:

    {"status":"ok", "data":....}

If operation has had some mistakes

    {"status":"error", "message": "..."}

More than one operation can be executed while socket is open.

### Put

Insert a new element into a bank.

Required parameters:

* op: Fixed to "put"
* bank: The bank name
* key: Key of entry
* value: value of entry

Optional parameters:

* lifetime: Number of seconds will be active this entry. If it is not specified
or it is 0 then the lifetime of entry is forever unless a client delete or replace it.

Example:

    {"op":"put","bank":"1","key":"test1","value":"test1v","lifetime":1}

### Get

Get an element from a bank

* op: Fixed to "get"
* bank: The bank name
* key: The key of entity

Example:

    {"op":"get","bank":"1","key":"test1"}

### Touch

Reset the timeout of an element

* op: Fixed to "touch"
* bank: The bank name
* key: The key of entity

Example:

    {"op":"touch","bank":"1","key":"test1"}


### Bank reset

Remove all elements of the bank. 

* op: Fixed to "bank.reset"
* bank: The bank name

### Bank keys

Get all the keys of the bank

* op: Fixed to "bank.reset"
* bank: The bank name

Example:

    {"op":"bank.reset","bank":"1"}

