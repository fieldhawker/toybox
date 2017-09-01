# -*- coding: utf-8 -*-

import sys
import os
import requests

sys.path.append(os.path.dirname(
    os.path.abspath(__file__)) + '/../toybox/toybox')
import settings

from bs4 import BeautifulSoup

from logging import getLogger
logger = getLogger(__name__)

import codecs

import feedparser
import feedgenerator
import pytz
from dateutil import parser

import time
from time import mktime
from datetime import datetime, timedelta

import re
import unicodedata
import random


class ScrapingService():

    URL_BLUEIMPULSE = 'http://www.mod.go.jp/asdf/pr_report/blueimpulse/schedule/'

    def __init__():

        pass

    def get_blueimpulse_schedule():

        logger.info('-- START ---')

        file_path = os.path.join(
            settings.STATIC_PATH, 'xml', 'blueimpulse.xml')

        feed = feedparser.parse(file_path)

        results = []
        for entry in feed.entries:

            result = {}

            result['title'] = entry.title
            result['link'] = entry.link
            result['description'] = entry.description
            result['pubdate'] = parser.parse(entry.published)

            # 画像はランダム
            images = ['https://scontent.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/21149002_341616412952601_552102897551147008_n.jpg',
            'https://scontent.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/21149306_119198935480166_625130960924442624_n.jpg',
            'https://scontent.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/21149639_118676192189557_7656973884633120768_n.jpg']
            num = random.randint(0,2)
            result['image'] = images[num]



            results.append(result)

        logger.info('-- END ---')

        return results


    def generate_blueimpulse_schedule(url=URL_BLUEIMPULSE):

        # http://127.0.0.1:8000/static/xml/blueimpulse.xml

        logger.info('-- START ---')

        # 入出力ファイルは以下だけ
        file_path = os.path.join(
            settings.STATIC_PATH, 'xml', 'blueimpulse.xml')

        timezone = pytz.timezone("Asia/Tokyo")
        nowdate = datetime.utcnow().astimezone(timezone)

        # 現在時間 nowdate

        # 差分比較のため現状のfeedを取得
        pre_feed = feedparser.parse(file_path)

        # 前回の更新時間 parser.parse(pre_feed.feed.updated).astimezone(timezone)

        # TODO: 踏み台にならないようにある程度の周期でのみ動作する感じに
        if 1 >= 2:
            logger.info('-- END has not passd 10 minutes. ---')
            return result

        # 最新のスケジュールを拾う
        soup = ScrapingService._request_blueimpulse_schedule(url)

        result = ''
        entries = []
        for row in soup.find_all('tr'):

            names = ['date', 'place', 'title']
            tds = row.find_all('td')

            entry = {}
            for (name, cell) in zip(names, tds):
                entry[name] = cell.get_text().strip()

            if len(entry) != 0:

                # 年が無いので付与
                entry['date'] = ScrapingService._convert_md_to_ymd(entry['date'])

                # 出力のタグ構成を今後決めよう
                entry['link'] = ''
                entry['description'] = entry['date'] + ' ' + entry['place']
                entry['pubdate'] = nowdate

                for pre_entry in pre_feed.entries:

                    # 同名タイトルが前回のFEEDにあれば前回のものを使おう
                    # 更新したものだけを残す感じにする場合はここでappendしない感じで

                    if entry['title'] == pre_entry.title:
                        entry['link'] = pre_entry.link
                        entry['description'] = pre_entry.description
                        entry['pubdate'] = parser.parse(pre_entry.published)
                        break

                entries.append(entry)

        # 取得できた情報があればRSS生成
        if len(entries) != 0:

            title = u"タイトル"
            link = "http://test.example.com"
            feed_url = "hhttp://test.example.com/static/xml/blueimpulse.xml"
            description = u"BlueImpulseのスケジュールです"
            language = "ja"
            author_name=u'ブログの著者'

            # フィードを生成
            feed = feedgenerator.Rss201rev2Feed(
                title=title, link=link, feed_url=feed_url,
                description=description, language=language,
                author_name=author_name)

            for entry in entries:

                title = entry["title"]
                link = entry["link"]
                description = entry["description"] if "description" in entry else None
                pubdate = entry["pubdate"]
                feed.add_item(
                    title=title, link=link, description=description, pubdate=pubdate, unique_id=link)

            # ファイルへの出力は切り出し
            ret = ScrapingService._export_blueimpulse_schedule_file(file_path, feed)

            result = feed.writeString("utf-8")

        logger.info('-- END ---')

        return result

    def _request_blueimpulse_schedule(url=URL_BLUEIMPULSE):

        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        return soup

    def _export_blueimpulse_schedule_file(file_path, feed):

        f = codecs.open(file_path, 'w+', 'utf-8')
        f.write(feed.writeString("utf-8"))
        f.close()

        return 1

    def _convert_md_to_ymd(md):

        ymd = md
        if (re.search(r"^.*月.*日.*$", md)):
            month = md.split('月',1)[0].strip()
            day = md.split('日',1)[0].strip().split('月',1)[1].strip()

            month = unicodedata.normalize('NFKC', month)
            day = unicodedata.normalize('NFKC', day)

            year = datetime.today().year
            now_month = datetime.today().month

            # 今が１月から３月
            if (now_month <= 3):
                # ４月から１２月は去年
                if (4 <= int(month)):
                    year = year - 1

            # 今が４月から１２月
            else:
                # １月から３月は来年
                if (int(month) <= 3):
                    year = year + 1

            ymd = str(datetime(year, int(month), int(day)))

        return ymd

    def get_link(url):

        logger.info('-- START ---')

        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')

        result = []
        for a in soup.find_all('a'):
            result.append(a.get('href'))

        logger.info('-- END ---')

        return result
