# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
@login_required
def home(request):
    template = 'base/base.html'
    return render(request,template_name=template)