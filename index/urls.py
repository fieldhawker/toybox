from django.conf.urls import url
from index import views

urlpatterns = [
    # インデックス
    url(r'^', views.index, name='index'),       # トップ
    url(r'^top/$', views.index, name='index'),   # トップ
    url(r'^index/$', views.index, name='index'), # トップ
]
