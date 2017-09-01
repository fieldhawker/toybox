# -*- coding: utf-8 -*-

import sys,os,io

import unittest
from unittest import mock

from services import scraping_service

from bs4 import BeautifulSoup

import random

class TestScrapingService(unittest.TestCase):

    # helloworld.
    def test_main(self):

        url = 'https://news.google.com/news/?ned=jp&hl=ja'

        # result = scraping_service.ScrapingService.get_link(url)
        # print(result)

        source_str = 'abcdefghijklmnopqrstuvwxyz'
        prefix = "".join([random.choice(source_str) for x in range(10)])

        xml =  \
            '<table>  \
            <tr><td>　３月２２日（日）</td><td>bbb</td><td>%sccc</td></tr> \
            <tr><td>　８月　２日（火）</td><td>eee</td><td>%sfff</td></tr> \
            </table>' % (prefix, prefix)
        soup = BeautifulSoup(xml, 'html.parser')

        入出力共にMock
        with \
            mock.patch('scraping_service.ScrapingService._request_blueimpulse_schedule', return_value=soup) as m1, \
            mock.patch('scraping_service.ScrapingService._export_blueimpulse_schedule_file', return_value=1) as m2:
        # 入力だけMock
        # with \
        #     mock.patch('scraping_service.ScrapingService._request_blueimpulse_schedule', return_value=soup) as m1:
        # 出力だけMock
        # with \
        #     mock.patch('scraping_service.ScrapingService._export_blueimpulse_schedule_file', return_value=1) as m1:

        # Mockを使用しない
        # with \
        #     mock.patch('scraping_service.ScrapingService.get_link', return_value=1) as m1:

            result = scraping_service.ScrapingService.generate_blueimpulse_schedule()

            self.assertIn('<title>%sccc</title>' % (prefix), result)
            self.assertIn('<description>2018-03-22 00:00:00 bbb</description>', result)
            self.assertIn('<title>%sfff</title>' % (prefix), result)
            self.assertIn('<description>2017-08-02 00:00:00 eee</description>', result)

if __name__ == "__main__":
    unittest.main()
