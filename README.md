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
* Python 2 and 3 compatible

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

    python3 server.py

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



## Operations

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

Example:

    {"op":"bank.reset","bank":"1"}

### Bank keys

List all the keys of the bank

* op: Fixed to "bank.keys"
* bank: The bank name

Example:

    {"op":"bank.keys","bank":"1"}


### Bank LIST

List all bank names

* op: Fixed to "bank.list"

Example:

    {"op":"bank.list"}

## API

With Cache Server, there are a RESTful API. 

This is optional and only interesting if you don't want to access directly to 
Server Cache Port. 

### Configuration file

A config.json file is required. It must include:

* SERVER_IP : IP of the server
* SERVER_PORT : Port of the server

Example:

    {
        "SERVER_IP" : "127.0.0.1",
        "SERVER_PORT" : 10001
    }

### Execution

To execute use this:

    python3 server.py

On console will appear the initialization

    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    * Restarting with stat
    * Debugger is active!

### Operations



#### Set an entry

* URL : /bank/\<bank\>/entry/\<key\>
* Method : POST
* Data : Values to store


#### Get an entry

* URL : /bank/\<bank\>/entry/\<key\>
* Method : GET

#### Touch and entry

* URL : /bank/\<bank\>/entry/\<key\>?op=touch
* Method : PUT

#### Get all entries

* URL : /bank/\<bank\>/entries
* Method : GET

#### Get all banks

* URL : /banks
* Method : GET

#### Clear a bank

* URL : /bank/\<bank\>?op=reset
* Method : PUT
    

## Create your own client

A python client can be created using Addons/Client.py that eases this task.

### Inicialization

First, a client object is required. It needs the cache IP and Port

    client=Client(<SERVER_IP>,<SEVER_PORT>)


### Operations


#### Add or replace a entry

    entry_set(self,bank,key,value,lifetime=0)
      
#### Get an entry

    entry_get(self,bank,key)
        
#### Touch an entry (Update the timeout of an entry)

    entry_touch(self,bank,key)
      
#### Get all entries of a bank (only keys)
    
    bank_keys(self,bank)

#### Reset a bank (Remove all entries)
    
    bank_reset(self, bank)

#### Get the list of banks

    bank_list(self)


### General operations

All operations of Cache server can be solved with the list of operations above. 
Although these are the general operations you can use too

#### Send a generic message to cache system

    send(self,msg):

#### Recieve a generic response from cache system.

    receive(self):
       
#### Send an operation to cache system, and wait for any response

    sendOp(self,op)


## Performance Study

A AWS instance has been used with these features:

- 512 Mb Ram
- 512 Mb Swap SSD
- 1 vCPU

Python 3 has been used to run these studies


### Study 1

In this test cache speed time is checked. Using testCache.py 

The client send 100.000 operations in each test. Each test is repeated 9 times to
get and Adverage time. The tests are:

* Test 1: 100.000 put operations
* Test 2: 100.000 get operations

Results:

|        |   1  |   2  |   3  |   4  |   5  |   6  |   7  |   8  |   9  |  Adv |   Per operation   |
|--------|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:-----------------:|
| Test 1 | 0,13 | 0,13 | 0,13 | 0,14 | 0,13 | 0,13 | 0,13 | 0,14 | 0,13 | 0,12 | 0,001 miliseconds |
| Test 2 | 0,22 | 0,23 | 0,23 | 0,23 | 0,23 | 0,23 | 0,22 | 0,23 | 0,23 | 0,21 | 0,002 miliseconds |

* Test 1 (get): 828.859 operations per second
* Test 2 (put): 485.514 operations per second


### Study 2

In this test response time is checked. One server and one client in the same 
machine to reduce the impact of connection latency

The client send 10.000 operations in each test. Each test is repeated 9 times to
get and Adverage time. The tests are:

* Test 1: In one connection to server, send 10.000 put operations
* test 2: Send 10.000 put operations opening and closing the connections
* Test 3: In one connection to server, send 10.000 get operations

Results:

|        |   1  |   2  |   3  |   4  |   5  |   6  |   7  |   8  |   9  |  Adv |   Per operation   |
|--------|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:-----------------:|
| Test 1 | 0,99 | 1,01 | 1,02 | 1,04 | 1,00 | 1,03 | 0,97 | 0,98 | 1,00 | 0,90 | 0,09 miliseconds  |
| Test 2 | 2,44 | 2,47 | 2,52 | 2,55 | 2,54 | 2,55 | 2,45 | 2,38 | 2,48 | 2,24 | 0,22 miliseconds  |
| Test 3 | 0,85 | 0,86 | 0,88 | 0,88 | 0,89 | 0,87 | 0,84 | 0,83 | 0,86 | 0,78 | 0,078 miliseconds |

* Test 1 (put): 12.871 operations per second
* Test 2 (get): 11.064 operations per second
* Test 3 (get with reconnections): 4.468 operations per second