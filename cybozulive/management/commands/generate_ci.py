from django.core.management.base import BaseCommand, CommandError
from services import cybozulive_service

# command : python manage.py generate_ci

class Command(BaseCommand):
    help = 'not arts.'


    """ Main """
    def handle(self, *args, **options):

        cs = cybozulive_service.CybozuliveService

        # group_name = cs.DEFAULT_POST_GROUP_NAME
        # topic_name = cs.DEFAULT_POST_TOPIC_NAME

        group_name = u'(株)エス・イー・プロジェクト'
        topic_name = u'いんふぉめーしょん'

        message = """\
[企業理念・経営理念]
　人づくりのすすめ
　● 創造と挑戦
　● 創造的発想を啓発し、革新的経営を目指せ
　● 積極思考を増長し、挑戦する意欲を高めよ

[経営ビジョン]
人と技術力の成長を通して、企業としての基盤を確固たるものにする
技術力あるSierを目指し、３年以内に売上１０億円を実現します
社会の変化に柔軟に対応し、１０年後も発展し続ける会社を目指します
社員が正当に評価され、自己実現できる会社を目指します\
"""

        result = cs.post_message_bulletin_board(
            group_name, topic_name, message)

        return result

        # ここに実行したい処理を書く
        # print("カスタムコマンドを実行")
