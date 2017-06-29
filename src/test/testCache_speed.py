# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "ilausuch"
__date__ = "$13-jun-2017 20:33:29$"


import sys
import os
sys.path.append(os.path.abspath("../Core"))
sys.path.append(os.path.abspath("../Addons"))

from Timer import Timer
from Cache import Cache, CacheItem

if __name__ == "__main__":
    cache=Cache()
    
    count=100000
    timer=Timer()
    
    for i in range(0,count):
        cache.put("Bank1",CacheItem(i,i))
    
    print ("{0} puts in {1} seconds".format(count,timer.end()))
    
    
    timer=Timer()
    
    for i in range(0,count):
        cache.get("Bank1",i)
    
    print ("{0} gets in {1} seconds".format(count,timer.end()))
