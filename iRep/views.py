# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from iRep.forms import SalesForceForm


@login_required
def home(request):
    template = 'base/base.html'
    return render(request,template_name=template)


@login_required
def AddSalesForce(request):
    template = 'sales_force/details.html'
    form = SalesForceForm(request.POST or None,request.FILES or None,user_instance=request.user)
    if form.is_valid():
        form.save(user=request.user)
        return redirect(reverse('index'))
    return render(request,template_name=template,context={'form':form})
