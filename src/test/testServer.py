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
    
    print sendOp(sock,'{"op":"put","bank":"1","key":"test1","value":"test1v","lifetime":1}')
    print sendOp(sock,'{"op":"get","bank":"1","key":"test1"}')
    time.sleep(2)
    print sendOp(sock,'{"op":"get","bank":"1","key":"test1"}')
    

if __name__ == "__main__":
    main()
