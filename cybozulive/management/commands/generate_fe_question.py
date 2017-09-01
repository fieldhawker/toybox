from django.core.management.base import BaseCommand, CommandError
from services import cybozulive_service
from services import scraping_service

# command : python manage.py generate_fe_question

class Command(BaseCommand):
    help = 'not arts.'

    # 投稿先グループが未指定の場合に使用するグループ名称
    DEFAULT_POST_GROUP_NAME = u'検証用グループ'
    DEFAULT_POST_TOPIC_NAME = u'過去問'
    DEFAULT_POST_MESSAGE = u'テスト投稿 by python'

    """ Main """
    def handle(self, *args, **options):

        cs = cybozulive_service.CybozuliveService
        ss = scraping_service.ScrapingService

        message = ss.get_fe_shiken_question()

        if message is None:
            print('message is None.')
            return False

        result = cs.post_message_bulletin_board(
            cs.DEFAULT_POST_GROUP_NAME,
            cs.DEFAULT_POST_TOPIC_NAME,
            message)

        print(result)
        return True

        # ここに実行したい処理を書く
        # print("カスタムコマンドを実行")
