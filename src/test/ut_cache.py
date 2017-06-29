'''
	Multi-thread Cache system
	LICENSE MIT @2017 Ivan LAusuch <ilausuch@gmail.com>
        
        Cache test
'''
__author__ = "ilausuch"
__date__ = "$13-jun-2017 20:33:29$"

import unittest
import sys
import os
import time

sys.path.append(os.path.abspath("../Core"))
sys.path.append(os.path.abspath("../Addons"))

from Cache import Cache, CacheItem

class TestStringMethods(unittest.TestCase):

    def test_000_basic(self):
        cache=Cache()
        cache.put("Bank1",CacheItem("key1","val1"))
        cache.put("Bank2",CacheItem("key1","val2"))
        self.assertEqual(cache.get("Bank1","key1").value, 'val1')
        self.assertEqual(cache.get("Bank2","key1").value, 'val2')
        
    def test_010_getNotExists(self):
        cache=Cache()
        
        with self.assertRaises(Exception) as context:
            cache.get("Bank1","key1")
        
        self.assertTrue("Key key1 doesn't exist" in str(context.exception))
        
    
    def test_020_banks(self):
        cache=Cache()
        cache.put("Bank1",CacheItem("key1","val1"))
        cache.put("Bank2",CacheItem("key1","val2"))
        v=cache.getBanks()
        self.assertIn("Bank1", v)
        self.assertIn("Bank2", v)
        
    def test_030_keys(self):
        cache=Cache()
        cache.put("Bank1",CacheItem("key1","val1"))
        cache.put("Bank1",CacheItem("key2","val2"))
        v=cache.getBank("Bank1").keys()
        self.assertIn("key1", v)
        self.assertIn("key2", v)
 
    def test_040_delete(self):
        cache=Cache()
        cache.put("Bank1",CacheItem("key1","val1"))
        cache.put("Bank1",CacheItem("key2","val2"))
        cache.delete("Bank1","key1")
        v=cache.getBank("Bank1").keys()
        self.assertNotIn("key1", v)
        self.assertIn("key2", v)
        
    def test_050_deleteNotExists(self):
        cache=Cache()
        
        with self.assertRaises(Exception) as context:
            cache.delete("Bank1","key1")
            
        self.assertTrue("Key key1 doesn't exist" in str(context.exception))
 
    def test_060_reset(self):
        cache=Cache()
        cache.put("Bank1",CacheItem("key1","val1"))
        cache.put("Bank1",CacheItem("key2","val2"))
        cache.getBank("Bank1").reset()
        self.assertEqual(cache.getBank("Bank1").keys(), [])
 
    def test_070_timeout(self):
        cache=Cache()
        cache.put("Bank1",CacheItem("key1","val1",2))
        time.sleep(1)
        cache.touch("Bank1","key1")
        time.sleep(1)
        self.assertIsNotNone(cache.get("Bank1","key1"))
        time.sleep(1)
        
        with self.assertRaises(Exception) as context:
            cache.get("Bank1","key1")
        
        self.assertTrue("Key key1 doesn't exist" in str(context.exception))


if __name__ == '__main__':
    unittest.main()