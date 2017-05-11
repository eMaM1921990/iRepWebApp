# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from iRep.forms import SalesForceForm


@login_required
def home(request):
    template = 'base/base.html'
    return render(request,template_name=template)


@login_required
def salesForceDetails(request):
    template = 'sales_force/details.html'
    form = SalesForceForm(request.POST or None,request.FILES or None,user_instance=request.user)
    if form.is_valid():
        pass

    return render(request,template_name=template,context={'form':form})
