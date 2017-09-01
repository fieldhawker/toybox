from __future__ import unicode_literals

# Create your views here.
# -*- coding: utf-8 -*-
from django.utils.encoding import python_2_unicode_compatible
from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@python_2_unicode_compatible
class Index(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'templates/accounts/index.html')
