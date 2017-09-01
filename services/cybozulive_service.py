# -*- coding: utf-8 -*-

import sys
import os
import json
import requests

sys.path.append(os.path.dirname(
    os.path.abspath(__file__)) + '/../toybox')
import settings

from bs4 import BeautifulSoup

from logging import Formatter, getLogger, FileHandler, StreamHandler, DEBUG

logger = getLogger(__name__)
# if not logger.handlers:
#     log_path = os.path.dirname(os.path.abspath(
#         __file__)) + r'/../logs/unittest.log'
#     formatter = Formatter(
#         '[%(asctime)s][%(levelname)s](%(filename)s:%(lineno)s %(funcName)s) %(message)s')
#
#     fileHandler = FileHandler(log_path)
#     fileHandler.setLevel(DEBUG)
#     fileHandler.setFormatter(formatter)
#     streamHander = StreamHandler()
#     streamHander.setLevel(DEBUG)
#     streamHander.setFormatter(formatter)
#     logger.setLevel(DEBUG)
#     logger.addHandler(fileHandler)
#     logger.addHandler(streamHander)
# ----------
# cybozulive
# ----------
import oauth2
import urllib
import httplib2


class CybozuliveService():

    # 投稿先グループが未指定の場合に使用するグループ名称
    DEFAULT_POST_GROUP_NAME = u'自分用グループ'
    REPLACE_GROUP_ID_WORD = 'GROUP,'
    DEFAULT_POST_TOPIC_NAME = u'メモするトピ'
    DEFAULT_POST_MESSAGE = u'テスト投稿 by python'


    ACCESS_TOKEN_URL = 'https://api.cybozulive.com/oauth/token'
    GROUP_ID_URL = 'https://api.cybozulive.com/api/group/V2'
    TOPIC_ID_URL = 'https://api.cybozulive.com/api/board/V2'
    COMMENT_URL = 'https://api.cybozulive.com/api/comment/V2'

    CONSUMER_TOKEN = {
        'key': settings.CONSUMER_TOKEN_KEY,
        'secret': settings.CONSUMER_TOKEN_SECRET
    }

    USER_ACCOUNT = {
        'username': settings.USER_ACCOUNT_USERNAME,
        'password': settings.USER_ACCOUNT_PASSWROD,
        'mode': 'client_auth'
    }
    #
    # # 投稿先グループが未指定の場合に使用するグループ名称
    # DEFAULT_POST_GROUP_NAME = u'自分用グループ'
    # REPLACE_GROUP_ID_WORD = 'GROUP,'
    # DEFAULT_POST_TOPIC_NAME = u'メモするトピ'
    # DEFAULT_POST_MESSAGE = u'テスト投稿 by python'


    # ----------
    # simpleApi
    # ----------
    HOST = "news.yahoo.co.jp"
    PORT = "80"
    PATH = '/pickup/sports/rss.xml'
    DEFAULT_HEADERS = {'Content-Type': 'application/json'}

    access_token = {}

    @classmethod
    def post_message_bulletin_board(self, group_name=DEFAULT_POST_GROUP_NAME, topic_name=DEFAULT_POST_TOPIC_NAME, message=DEFAULT_POST_MESSAGE):
        """サイボウズLiveの掲示板にメッセージを投稿する関数
        """

        logger.info('-- START ---')

        token = self.get_access_token()
        logger.info(token)

        group_id = self.get_group_id(token, group_name)
        logger.info(group_id)

        topic_id = self.get_topic_id(token, group_id, topic_name)
        logger.info(topic_id)

        result = self.post_message(token, group_id, topic_id, message)
        logger.info(result)

        logger.info('-- END ---')

        return result

    @classmethod
    def request_token(self):

        consumer = oauth2.Consumer(
            self.CONSUMER_TOKEN['key'], self.CONSUMER_TOKEN['secret'])

        client = oauth2.Client(consumer)
        client.add_credentials(
            self.USER_ACCOUNT['username'], self.USER_ACCOUNT['password'])
        client.authorizations

        client.set_signature_method = oauth2.SignatureMethod_HMAC_SHA1()

        params = {}
        params["x_auth_username"] = self.USER_ACCOUNT['username']
        params["x_auth_password"] = self.USER_ACCOUNT['password']
        params["x_auth_mode"] = self.USER_ACCOUNT['mode']

        resp, token = client.request(
            self.ACCESS_TOKEN_URL, method="POST", body=urllib.parse.urlencode(params))

        response = {}
        response['resp'] = resp
        response['token'] = token
        logger.info(response)
        return response

    @classmethod
    def get_access_token(self):
        """サイボウズLiveの認証トークンを取得する関数
        """

        logger.info('-- START ---')

        token = {}

        try:

            response = self.request_token()

            if response['resp']['status'] == '200':
                # oauth_token        : xxxxx
                # oauth_token_secret : xxxxx

                token = urllib.parse.parse_qs(
                    response['token'].decode('utf-8'))
                token['oauth_token'] = token['oauth_token'][0]
                token['oauth_token_secret'] = token['oauth_token_secret'][0]
                logger.info(token)

        except Exception as e:
            token['oauth_token'] = ''
            token['oauth_token_secret'] = ''

        logger.info('-- END ---')

        return token

    @classmethod
    def get_group_id(self, token, group_name=DEFAULT_POST_GROUP_NAME):
        """サイボウズLiveの対象のグループのグループIDを取得する関数
        """
        logger.info('-- START ---')

        group_id = ''
        params = {}

        response = self.request_cybozulive('GET', token, self.GROUP_ID_URL)
        logger.info(response)

        if response['header']['status'] == '200':

            soup = BeautifulSoup(response['body'], 'lxml')

            for entry in soup.find_all('entry'):

                logger.debug(entry.find('title').text.encode('utf-8'))
                logger.debug(group_name.encode('utf-8'))

                if entry.find('title').text == group_name:
                    group_id = entry.find('id').text.replace(
                        self.REPLACE_GROUP_ID_WORD, '')

        # try:
        #     consumer = oauth2.Consumer(
        #         CONSUMER_TOKEN['key'], CONSUMER_TOKEN['secret'])
        #     token = oauth2.Token(
        #         token['oauth_token'], token['oauth_token_secret'])
        #
        #     params = {}
        #     logger.debug(consumer)
        #     logger.debug(token)
        #
        #     client = oauth2.Client(consumer, token)
        #
        #     client.authorizations
        #     client.set_signature_method = oauth2.SignatureMethod_HMAC_SHA1()
        #     header, body = client.request(
        #         'https://api.cybozulive.com/api/group/V2')
        #
        #     logger.debug(header)
        #
        #     if header['status'] == '200':
        #
        #         soup = BeautifulSoup(body, 'lxml')
        #
        #         for entry in soup.find_all('entry'):
        #
        #             logger.debug(entry.find('title').text.encode('utf-8'))
        #             logger.debug(group_name.encode('utf-8'))
        #
        #             if entry.find('title').text == group_name:
        #                 group_id = entry.find('id').text.replace(
        #                     REPLACE_GROUP_ID_WORD, '')
        #
        # except Exception as e:
        #     import traceback
        #     traceback.print_exc()

        logger.info('-- END ---')
        return group_id

    @classmethod
    def get_topic_id(self, token, group_id, topic_name=DEFAULT_POST_TOPIC_NAME):
        """サイボウズLiveの対象の掲示板の掲示板IDを取得する関数
        """
        logger.info('-- START ---')

        topic_id = ''
        params = {"group".encode('utf-8'): group_id.encode('utf-8')}
        logger.debug(params)

        url = self.TOPIC_ID_URL + '?' + urllib.parse.urlencode(params)
        logger.debug(url)
        response = self.request_cybozulive('GET', token, url)

        logger.debug(response)

        if response['header']['status'] == '200':

            soup = BeautifulSoup(response['body'], 'lxml')

            for entry in soup.find_all('entry'):

                logger.debug(entry.find('title').text.encode('utf-8'))
                logger.debug(topic_name.encode('utf-8'))

                if entry.find('title').text == topic_name:
                    topic_id = entry.find('id').text

        logger.info('-- END ---')
        return topic_id

    @classmethod
    def post_message(self, token, group_id, topic_id, message):
        """サイボウズLiveの指定のグループ指定の掲示板に投稿する関数
        """
        logger.info('-- START ---')

        result = 0

        xml_string = """\
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
xmlns:cbl="http://schemas.cybozulive.com/common/2010"
xmlns:cblCmnt="http://schemas.cybozulive.com/comment/2010">
<cbl:operation type="insert"/>
<id>{topic_id}</id>
<entry>
<summary type="text">{message}</summary>
<cblCmnt:replyTo>2</cblCmnt:replyTo>
</entry>
</feed>\
""".format(topic_id=topic_id, message=message)

        logger.debug(xml_string)

        result = self.request_cybozulive_with_xml(
            'POST', token, self.COMMENT_URL, xml_string)

        logger.info('-- END ---')
        return result

    @classmethod
    def request_cybozulive_with_xml(self, method, token, url=COMMENT_URL, xml_string=None):
        """サイボウズLiveへのリクエスト処理
        """
        logger.info('-- START ---')

        try:
            consumer = oauth2.Consumer(
                self.CONSUMER_TOKEN['key'], self.CONSUMER_TOKEN['secret'])
            token = oauth2.Token(
                token['oauth_token'], token['oauth_token_secret'])

            client = oauth2.Client(consumer, token)

            client.authorizations
            client.set_signature_method = oauth2.SignatureMethod_HMAC_SHA1()

            header, body = client.request(url, method, body=xml_string.encode('utf-8'), headers={
                                          'Content-Type': 'application/atom+xml; charset=utf-8'})

            logger.info(header)
            logger.info(body)
            if header['status'] == '200':

                result = 1
                response = {}
                response['header'] = header
                response['body'] = body

        except Exception as e:

            import traceback
            traceback.print_exc()

        logger.info('-- END ---')
        return result

    @classmethod
    def request_cybozulive(self, method, token, url, params=None):
        """サイボウズLiveへのリクエスト処理
        """
        logger.info('-- START ---')

        response = {}
        response['header'] = {}
        response['body'] = {}

        try:
            consumer = oauth2.Consumer(
                self.CONSUMER_TOKEN['key'], self.CONSUMER_TOKEN['secret'])
            token = oauth2.Token(
                token['oauth_token'], token['oauth_token_secret'])

            logger.debug(consumer)
            logger.debug(token)

            client = oauth2.Client(consumer, token)

            client.authorizations
            client.set_signature_method = oauth2.SignatureMethod_HMAC_SHA1()

            if params == None:
                header, body = client.request(url, method=method)
            else:

                header, body = client.request(
                    url, method=method, body=urllib.parse.urlencode(params))

            logger.debug(header)
            logger.debug(body)

            if header['status'] == '200':

                response['header'] = header
                response['body'] = body

        except Exception as e:
            import traceback
            traceback.print_exc()

        logger.info('-- END ---')
        return response

    def simple_api():
        """getリクエストで単純取得できるRSSの動作確認用
        """

        try:
            return requests.get("http://{0}:{1}{2}".format(HOST, PORT, PATH),
                                params={},
                                headers=DEFAULT_HEADERS)

        except Exception as e:
            return None
