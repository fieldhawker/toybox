# coding: utf-8
from django.conf.urls import url
from django.contrib.auth.views import login, logout_then_login
from accounts.views import Index

urlpatterns = [
    url(r'^', login, {'template_name': '../templates/accounts/login.html'}, name='login'),
    url(r'^login/$', login, {'template_name': '../templates/accounts/login.html'}, name='login'),
    url(r'^logout/$', logout_then_login, name='logout'),
    url(r'^index/$', Index.as_view(), name='account_index'),
]
