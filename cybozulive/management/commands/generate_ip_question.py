from django.core.management.base import BaseCommand, CommandError
from services import question_service

# command : python manage.py generate_ip_question

class Command(BaseCommand):
    help = 'not arts.'

    """ Main """
    def handle(self, *args, **options):

        qs = question_service.QuestionService

        result = qs.get_ip_shiken_question()

        return result

        # ここに実行したい処理を書く
        # print("カスタムコマンドを実行")
