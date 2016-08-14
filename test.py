# -*- coding: utf-8 -*-

import unittest
import requests


class APITestCase(unittest.TestCase):
    def test_zd_tickets(self):
        url = 'http://localhost:5000/zd?Date=2016-08-13&from=北京&to=杭州'
        r = requests.get(url)
        self.assertTrue(r.status_code == 200)

    def test_hc_tickets(self):
        url = 'http://localhost:5000/hc?Date=2016-08-15&from=北京&to=杭州&change=上海'
        r = requests.get(url)
        self.assertTrue(r.status_code == 200)

    def test_error(self):
        url = 'http://localhost:5000/hc?Date=2016-08-15&from=beijing&to=hangzhou&change=shanghai'
        r = requests.get(url)
        self.assertTrue(r.status_code == 400)

    def test_date(self):
        url = 'http://localhost:5000/hc?Date=2016-07-15&from=北京&to=杭州&change=上海'
        r = requests.get(url)
        self.assertTrue(r.status_code == 404)

if __name__ == '__main__':
    unittest.main()
