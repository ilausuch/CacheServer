# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "ilausuch"
__date__ = "$13-jun-2017 20:33:29$"

import sys
import os
sys.path.append(os.path.abspath("../Core"))

from Cache import Cache, CacheItem

if __name__ == "__main__":
    cache=Cache()
    
    cache.put("Bank1",CacheItem("key1","val1"))
    cache.put("Bank2",CacheItem("key1","val1.1"))
    cache.put("Bank2",CacheItem("key1","val1bis"))
    cache.put("Bank1",CacheItem("key2","val2"))
    print cache.get("Bank1","key1").value
    print cache.get("Bank1","key2").value
    print cache.get("Bank2","key1").value
