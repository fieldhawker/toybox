# coding: utf-8
from django.conf.urls import url
from event import views

urlpatterns = [
    # インデックス
    url(r'^$', views.index, name='index'),       # トップ
    url(r'^top/$', views.index, name='index'),   # トップ
    url(r'^index/$', views.index, name='index'), # トップ
]
