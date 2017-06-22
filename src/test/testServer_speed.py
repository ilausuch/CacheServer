import sys

__author__ = "ilausuch"
__date__ = "$13-jun-2017 20:05:19$"


sys.path.append( "../Addons" )

from Client import Client
from Timer import Timer


count=1000
    
def test1():
    print ("Test 1: Multiple entry set same connection (count={0})".format(count))
    
    client = Client("localhost", 10001)
    timer=Timer()
    
    for i in range(0,count):
        client.entry_set("test speed",i,i)
       
    client.close()
    print ("Seconds: {0}".format(timer.end()))
    

def test2():
    print ("Test 2: Multiple entry set opening/closing connection (count={0})".format(count))
    
    
    timer=Timer()
    
    for i in range(0,count):
        client = Client("localhost", 10001)
        client.entry_set("test speed",i,i)
        client.close()
       
    client.close()
    print ("Seconds: {0}".format(timer.end()))
    
def test3():
    print ("Test 3: Multiple entry get (count={0})".format(count))
    
    client = Client("localhost", 10001)
    timer=Timer()
    
    for i in range(0,count):
        client.entry_get("test speed",i)
        
    client.close()
    print ("Seconds: {0}".format(timer.end()))
    
    
def main():
    test1()
    test2()
    test3()
    
    
if __name__ == "__main__":
    main()
