# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from iRep.forms import SalesForceForm, SalesForceReportForm, ProductForm
from iRep.managers.Corp import CorpManager
from iRep.managers.Products import ProductManager
from iRep.managers.SalesForce import SalesForceManager
from iRep.models import SalesForce


@login_required
def home(request):
    template = 'base/base.html'
    return render(request, template_name=template)


@login_required
def AddSalesForce(request):
    template = 'sales_force/details.html'
    # Get Corp Info
    corp = CorpManager().get_corp_by_user(request.user)
    form = SalesForceForm(request.POST or None, request.FILES or None, user_instance=request.user, corp_instance=corp,
                          action=reverse('createSalesForce'))
    if form.is_valid():
        form.save(user=request.user)
        return redirect(reverse('index'))
    return render(request, template_name=template, context={'form': form, 'new': True})


@login_required
def ViewSalesForceDefault(request,slug):
    template = 'sales_force/list.html'
    context = {
        'salesForce': SalesForceManager().ListByUserCorp(slug=slug)
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
def AddProduct(request,slug):
    template = 'settings/products/details.html'
    form = ProductForm(request.POST or None,slug=slug,action=reverse('createProduct',kwargs={'slug':slug}))
    if form.is_valid():
        corporate = CorpManager().get_corp_form_user_profile(request.user)
        corporate= corporate.corporate
        print corporate
        form.save(user=request.user,corporate=corporate)
        return redirect(reverse('productList'))
    return render(request, template_name=template, context={'form': form, 'new': True})


@login_required
def ViewProduct(request, slug):
    template = 'settings/products/list.html'
    context = {
        'products': ProductManager().get_corp_products(slug=slug)
    }
    return render(request, template_name=template, context=context)
