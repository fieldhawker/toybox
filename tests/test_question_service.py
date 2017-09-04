# -*- coding: utf-8 -*-

import sys,os,io

import unittest
from unittest import mock

from services import question_service

from bs4 import BeautifulSoup

# import random

class TestQuestionService(unittest.TestCase):

    #
    def test_main(self):

        with \
            mock.patch('scraping_service.ScrapingService.get_fe_shiken_question', return_value=None) as m1:

            result = question_service.QuestionService.get_fe_shiken_question()
            self.assertEqual(result, False)

            xml =  '''
            <div class="kako">
<div class="mondai">1文字が，縦48ドット，横32ドットで表される2値ビットマップのフォントがある。文字データが8,192種類あるとき，文字データ全体を保存するために必要な領域は何バイトか。ここで，1Mバイト＝1,024kバイト，1kバイト＝1,024バイトとし，文字データは圧縮しないものとする。</div>
<div class="anslink">平成25年秋期　基本情報技術者 問11 [テクノロジ系]</div>
<div class="ansbg"><ul class="selectList cf col1">
<li class="lia">192k</li><li class="lii">1.5M</li><li class="liu">12M</li><li class="lie">96M</li>
</ul></div>
<div class="img_margin"><a href="./kakomon/25_aki/q11.html"><i class="ansbtn"></i></a></div></div>'''

            soup = BeautifulSoup(xml, 'html.parser')

        with \
            mock.patch('scraping_service.ScrapingService.get_fe_shiken_question', return_value=soup) as m1, \
            mock.patch('cybozulive_service.CybozuliveService.post_message_bulletin_board', return_value=True) as m2:

            result = question_service.QuestionService.get_fe_shiken_question()
            self.assertEqual(result, True)

if __name__ == "__main__":
    unittest.main()
