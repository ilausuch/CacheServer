import socket
import time

__author__ = "ilausuch"
__date__ = "$13-jun-2017 20:05:19$"


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
    
    print "---------------------------------------------"
    print " Test 1. Creation of a 1 second lifetime element"
    print "---------------------------------------------"
    
    print "* Creation of a new element test1 on bank 1 with 1 second of life"
    print sendOp(sock,'{"op":"put","bank":"1","key":"test1","value":"test1v","lifetime":1}')
    
    print "* Getting the value of this element"
    print sendOp(sock,'{"op":"get","bank":"1","key":"test1"}')
    
    print "* Waiting 2 seconds"
    time.sleep(2)
    
    print "* Get this element again, will be a key error, because of expiration"
    print sendOp(sock,'{"op":"get","bank":"1","key":"test1"}')
    
    
    print "---------------------------------------------"
    print " Test 2. Reset of the timeout"
    print "---------------------------------------------"
    
    print "* Creation of a new element test1 on bank 1 with 2 second of life"
    print sendOp(sock,'{"op":"put","bank":"1","key":"test1","value":"test1v","lifetime":2}')
    
    print "* Waiting 1 seconds"
    time.sleep(1)
    
    print "* Touch this element to reset the timeout "
    print sendOp(sock,'{"op":"touch","bank":"1","key":"test1"}')
    
    print "* Waiting 1 seconds again"
    time.sleep(1)
    
    print "* Touch this element to reset the timeout "
    print sendOp(sock,'{"op":"touch","bank":"1","key":"test1"}')
    
    print "* Waiting 1 seconds again"
    time.sleep(1)
    
    print "* Get this element again"
    print sendOp(sock,'{"op":"get","bank":"1","key":"test1"}')
    
    print "* Waiting 2 seconds again"
    time.sleep(2)
    
    print "* Get this element again, it will be erased"
    print sendOp(sock,'{"op":"get","bank":"1","key":"test1"}')


    print "---------------------------------------------"
    print " Test 3. Bank clear"
    print "---------------------------------------------"
    
    print "* Creation of a new element test1 on bank 1 with 2 second of life"
    print sendOp(sock,'{"op":"put","bank":"1","key":"test1","value":"test1v"}')
    
    print "* Creation of a new element test2 on bank 1 with 2 second of life"
    print sendOp(sock,'{"op":"put","bank":"1","key":"test2","value":"test2v"}')
    
    print "* Get element test1"
    print sendOp(sock,'{"op":"get","bank":"1","key":"test1"}')
    
    print "* Get element test2"
    print sendOp(sock,'{"op":"get","bank":"1","key":"test2"}')
    
    print "* Clear bank"
    print sendOp(sock,'{"op":"bank.reset","bank":"1"}')
    
    print "* Get element test1, it will fail"
    print sendOp(sock,'{"op":"get","bank":"1","key":"test1"}')
    
    print "* Get element test2, it will fail"
    print sendOp(sock,'{"op":"get","bank":"1","key":"test2"}')
    

if __name__ == "__main__":
    main()
