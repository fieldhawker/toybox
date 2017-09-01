from django.test import TestCase

# Create your tests here.
class EventTest(TestCase):


    def setUp(self):
        # unittest を使う場合、毎回 Client を生成する必要があります。
        # self.client = Client()

    def test_access(self):

        print('test!')
