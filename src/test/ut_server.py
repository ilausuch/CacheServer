# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import unittest
import sys
import os
import json
import time

sys.path.append(os.path.abspath("../Addons"))

from Client import Client


def checkInList(result, item):
    js = json.loads(result)
    if js["status"] != 'ok':
        return False

    return item in js["data"]


def checkError(result):
    js = json.loads(result)
    return js["status"] == 'error'


class Ut_serverTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client("localhost", 10001)
        self.ok = '{"status": "ok", "data": {}}'

    def tearDown(self):
        self.client.close()

    def test_000_basic(self):
        v = self.client.entry_set("Bank1", "key1", "value1")
        self.assertEqual(v, self.ok)

        v = self.client.entry_get("Bank1", "key1")
        self.assertEqual(v, '{"status": "ok", "data": "value1"}')

    def test_010_getNotExists(self):
        v = self.client.entry_get("Bank5", "key1")
        self.assertTrue(checkError(v))

    def test_020_banks(self):
        self.client.entry_set("Bank1", "key1", "value1")
        self.client.entry_set("Bank2", "key1", "value1")
        v = self.client.bank_list()
        self.assertTrue(checkInList(v, "Bank1"))
        self.assertTrue(checkInList(v, "Bank2"))

    def test_030_keys(self):
        self.client.entry_set("Bank1", "key1", "value1")
        self.client.entry_set("Bank2", "key2", "value1")
        v = self.client.bank_keys("Bank2")
        self.assertTrue(checkInList(v, "key1"))
        self.assertTrue(checkInList(v, "key2"))

    def test_040_delete(self):
        self.client.entry_set("Bank1", "key1", "value1")
        self.client.entry_set("Bank1", "key2", "value1")
        self.client.entry_delete("Bank1", "key1")
        v = self.client.bank_keys("Bank1")
        self.assertFalse(checkInList(v, "key1"))
        self.assertTrue(checkInList(v, "key2"))

    def test_050_deleteNotExists(self):
        v = self.client.entry_delete("Bank5", "key1")
        self.assertTrue(checkError(v))

    def test_060_reset(self):
        self.client.entry_set("Bank1", "key1", "value1")
        self.client.entry_set("Bank1", "key2", "value1")
        self.client.bank_reset("Bank1")
        v = self.client.bank_keys("Bank1")
        self.assertFalse(checkInList(v, "key1"))
        self.assertFalse(checkInList(v, "key2"))

    def test_070_timeout(self):
        self.client.entry_set("Bank1", "key1", "value1", 2)
        time.sleep(1)

        self.client.entry_touch("Bank1", "key1")
        time.sleep(1)

        v = self.client.entry_get("Bank1", "key1")
        self.assertEqual(v, '{"status": "ok", "data": "value1"}')
        time.sleep(1)

        v = self.client.entry_get("Bank1", "key1")
        self.assertTrue(checkError(v))

    def test_080_incr(self):
        v = self.client.entry_set("BankNum", "key1", 1)
        self.assertEqual(v, self.ok)

        v = self.client.entry_get("BankNum", "key1")
        self.assertEqual(v, '{"status": "ok", "data": 1}')

        v = self.client.entry_incr("BankNum", "key1", 1)
        self.assertEqual(v, '{"status": "ok", "data": 2.0}')

        v = self.client.entry_incr("BankNum", "key1", "a")
        self.assertEqual(
            v, '{"status": "error", "message": "The value must be an integer or a float"}')

        v = self.client.entry_set("BankNum", "key2", 1)
        self.assertEqual(v, self.ok)

        v = self.client.entry_incr("BankNum", "key2", 1)
        self.assertEqual(v, '{"status": "ok", "data": 2.0}')


if __name__ == '__main__':
    unittest.main()
