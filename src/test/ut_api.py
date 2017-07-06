'''
	Multi-thread Cache system
	LICENSE MIT @2017 Ivan LAusuch <ilausuch@gmail.com>
    API Test
'''

import unittest
import json
import requests

PATH = "http://localhost:8000/api/"


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
        pass

    def tearDown(self):
        pass

    def test_000_api_up(self):
        r = requests.get(PATH + '')
        self.assertEqual(r.status_code, 200)

    def test_001_set(self):
        r = requests.post(PATH + 'bank/bank1/entry/entry1',
                          headers={"Content-Type": "text / plain"},
                          data="value 1")
        self.assertEqual(r.status_code, 200)

    def test_002_get(self):
        r = requests.get(PATH + 'bank/bank1/entry/entry1')
        self.assertEqual(r.status_code, 200)
        r = r.json()
        self.assertEqual(r["status"], "ok")
        self.assertEqual(r["data"], "value 1")

    def test_003_keys(self):
        r = requests.post(PATH + 'bank/bank1/entry/entry1',
                          headers={"Content-Type": "text / plain"},
                          data="value 1")
        self.assertEqual(r.status_code, 200)

        r = requests.post(PATH + 'bank/bank1/entry/entry2',
                          headers={"Content-Type": "text / plain"},
                          data="value 2")
        self.assertEqual(r.status_code, 200)

        r = requests.get(PATH + 'bank/bank1/entries')
        self.assertEqual(r.status_code, 200)
        r = r.json()
        self.assertEqual(r["status"], "ok")
        self.assertIn("entry1", r["data"])
        self.assertIn("entry2", r["data"])

    def test_004_clear_bank(self):
        r = requests.put(PATH + 'bank/bank1?operation=reset')
        self.assertEqual(r.status_code, 200)

        r = requests.get(PATH + 'bank/bank1/entries')
        self.assertEqual(r.status_code, 200)
        r = r.json()

        self.assertEqual(r["status"], "ok")
        self.assertNotIn("entry1", r["data"])
        self.assertNotIn("entry2", r["data"])

    def test_005_banks(self):
        r = requests.post(PATH + 'bank/bank1/entry/entry1',
                          headers={"Content-Type": "text / plain"},
                          data="value 1")
        self.assertEqual(r.status_code, 200)

        r = requests.post(PATH + 'bank/bank2/entry/entry1',
                          headers={"Content-Type": "text / plain"},
                          data="value 1")
        self.assertEqual(r.status_code, 200)

        r = requests.get(PATH + 'banks')
        self.assertEqual(r.status_code, 200)
        r = r.json()

        self.assertEqual(r["status"], "ok")
        self.assertIn("bank1", r["data"])
        self.assertIn("bank2", r["data"])

    def test_005_error_get_unknownEntry(self):
        r = requests.get(PATH + 'bank/bank1/entry/unknownEntry')
        self.assertEqual(r.status_code, 400)

    def test_006_error_get_unknownBank(self):
        r = requests.get(PATH + 'bank/unknownBank/entry/unknownEntry')
        self.assertEqual(r.status_code, 400)

    def test_007_entries_unkwnowBank(self):
        r = requests.get(PATH + 'bank/unknownBank/entries')
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    print("It is going to check an api running on {}".format(PATH))
    unittest.main()
