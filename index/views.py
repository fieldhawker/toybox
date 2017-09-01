from django.shortcuts import render

# Create your views here.
import sys, os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../services')

from services import hello_service
from services import cybozulive_service

from django.http import HttpResponse

def index(request):

    one = 1

    return render(request,
                  'index/index.html',     # 使用するテンプレート
                  {'index': '', 'one': one})    # 引数
