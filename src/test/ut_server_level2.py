import unittest
import sys
import os
import json
import time
import socket

sys.path.append(os.path.abspath("../Addons"))

from Client import Client


class Ut_serverTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client("localhost", 10001)
        self.ok = '{"status": "ok", "data": {}}'

        self.listenner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listenner.connect(("localhost", 10002))

    def tearDown(self):
        self.client.close()
        self.listenner.close()

    def test_000_basic(self):
        v = self.client.entry_set("Bank1", "key1", "value1")
        self.assertEqual(v, self.ok)

        v = self.listenner.recv(2048).decode()
        self.assertEqual(
            v, '{"op": "put", "bank": "Bank1", "key": "key1", "value": "value1", "timeout": 0}')


if __name__ == '__main__':
    unittest.main()
