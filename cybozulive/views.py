from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from services import hello_service
from services import cybozulive_service


def index(request):
    return render(request,
                  'cybozulive/index.html',     # 使用するテンプレート
                  {'index': ''})    # 引数


# def postMessage(request):
#     """掲示板に投稿"""


    # oauth認証

    # 投稿

    # aaa = cybozuliveService.cybozuAuth()

    # return HttpResponse('インデックス')
    # return render(request,
    #               'cybozulive/index.html',     # 使用するテンプレート
    #               {'index': aaa})    # 引数
    # return HttpResponse('bbb')
