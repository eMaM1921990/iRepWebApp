# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from iRep.forms import SalesForceForm, SalesForceReportForm, ProductForm
from iRep.managers.SalesForce import SalesForceManager
from iRep.models import SalesForce


@login_required
def home(request):
    template = 'base/base.html'
    return render(request, template_name=template)


@login_required
def AddSalesForce(request):
    template = 'sales_force/details.html'
    form = SalesForceForm(request.POST or None, request.FILES or None, user_instance=request.user,
                          action=reverse('createSalesForce'))
    if form.is_valid():
        form.save(user=request.user)
        return redirect(reverse('index'))
    return render(request, template_name=template, context={'form': form, 'new': True})


@login_required
def ViewSalesForceDefault(request):
    template = 'sales_force/list.html'
    context = {
        'salesForce': SalesForceManager().ListByUser(request.user)
    }
    return render(request, template_name=template, context=context)


@login_required
def EditSalesForce(request, slug):
    template = 'sales_force/details.html'
    sales_force_instance = get_object_or_404(SalesForce, slug=slug)
    form = SalesForceForm(request.POST or None, request.FILES or None,
                          user_instance=request.user,
                          instance=sales_force_instance, action=reverse('editSalesForce', kwargs={'slug': slug}))
    reportForm = SalesForceReportForm()
    if form.is_valid():
        form.save(user=request.user)
        return redirect(reverse('index'))
    return render(request, template_name=template, context={'form': form, 'new': False, 'reportForm': reportForm})


@login_required
def AddProduct(request):
    template = 'settings/products/details.html'
    form = ProductForm(request.POST or None, user_instance=request.user, action=None)
    if form.is_valid():
        form.save()
        return redirect(reverse('productList'))
    return render(request, template_name=template, context={'form': form, 'new': False})


def ViewProduct(request):
    template = 'settings/products/list.html'
    context = {
        'products':
    }

