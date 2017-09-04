# -*- coding: utf-8 -*-

import sys
import os
import requests

from logging import getLogger
logger = getLogger('normal')

from services import cybozulive_service
from services import scraping_service


class QuestionService():

    # 投稿先グループが未指定の場合に使用するグループ名称
    DEFAULT_POST_GROUP_NAME = u'(株)エス・イー・プロジェクト'
    DEFAULT_POST_TOPIC_NAME = u'過去問題集'
    # DEFAULT_POST_GROUP_NAME = u'検証用グループ'
    # DEFAULT_POST_TOPIC_NAME = u'過去問'
    DEFAULT_POST_MESSAGE = u'テスト投稿 by python'

    def get_fe_shiken_question():

        logger.info('-- START ---')

        cs = cybozulive_service.CybozuliveService
        ss = scraping_service.ScrapingService

        message = ss.get_fe_shiken_question()

        if message is None:
            logger.info('message is None.')
            return False

        result = cs.post_message_bulletin_board(
            QuestionService.DEFAULT_POST_GROUP_NAME,
            QuestionService.DEFAULT_POST_TOPIC_NAME,
            message)

        logger.info('-- END ---')

        return result

    def get_ap_shiken_question():

        logger.info('-- START ---')

        cs = cybozulive_service.CybozuliveService
        ss = scraping_service.ScrapingService

        message = ss.get_ap_shiken_question()

        if message is None:
            logger.info('message is None.')
            return False

        result = cs.post_message_bulletin_board(
            QuestionService.DEFAULT_POST_GROUP_NAME,
            QuestionService.DEFAULT_POST_TOPIC_NAME,
            message)

        logger.info('-- END ---')

        return result

    def get_ip_shiken_question():

        logger.info('-- START ---')

        cs = cybozulive_service.CybozuliveService
        ss = scraping_service.ScrapingService

        message = ss.get_ip_shiken_question()

        if message is None:
            logger.info('message is None.')
            return False

        result = cs.post_message_bulletin_board(
            QuestionService.DEFAULT_POST_GROUP_NAME,
            QuestionService.DEFAULT_POST_TOPIC_NAME,
            message)

        logger.info('-- END ---')

        return result
