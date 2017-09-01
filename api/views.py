from django.shortcuts import render

# Create your views here.
# coding: utf-8

from django.http import HttpResponse

def index(request):
    return render(request,
                  'cybozulive/index.html',     # 使用するテンプレート
                  {'index': ''})    # 引数
