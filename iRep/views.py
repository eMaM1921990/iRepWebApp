# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse

from iRep.forms import SalesForceForm, SalesForceReportForm, ProductForm, BaseReportForm, ClientForm
from iRep.managers.Corp import CorpManager
from iRep.managers.Products import ProductManager
from iRep.managers.SalesForce import SalesForceManager
from iRep.models import SalesForce, Product


@login_required
def home(request):
    template = 'index.html'
    return render(request, template_name=template)


@login_required
def AddSalesForce(request):
    template = 'sales_force/details.html'
    # Get Corp Info
    corp = CorpManager().get_corp_by_user(request.user)
    print corp
    form = SalesForceForm(request.POST or None, request.FILES or None, user_instance=request.user, corp_instance=corp,
                          action=reverse('createSalesForce'))
    if form.is_valid():
        form.save(user=request.user)
        return redirect(reverse('index'))
    return render(request, template_name=template, context={'form': form, 'new': True})


@login_required
def ViewSalesForceDefault(request, slug):
    template = 'sales_force/list.html'
    context = {
        'salesForce': SalesForceManager().ListByUserCorp(slug=slug)
    }
    return render(request, template_name=template, context=context)


@login_required
def EditSalesForce(request, slug):
    template = 'sales_force/details.html'
    corp = CorpManager().get_corp_by_user(request.user)
    sales_force_instance = get_object_or_404(SalesForce, slug=slug)
    form = SalesForceForm(request.POST or None, request.FILES or None,
                          user_instance=request.user,
                          instance=sales_force_instance,
                          corp_instance=corp,
                          action=reverse('editSalesForce', kwargs={'slug': slug}))
    reportForm = SalesForceReportForm()
    if form.is_valid():
        form.save(user=request.user)
        return redirect(reverse('index'))
    return render(request, template_name=template, context={'form': form, 'new': False, 'reportForm': reportForm})


@login_required
def AddProduct(request, slug):
    template = 'settings/products/details.html'
    form = ProductForm(request.POST or None, slug=slug, action=reverse('createProduct', kwargs={'slug': slug}))
    if form.is_valid():
        corporate = CorpManager().get_corp_form_user_profile(request.user)
        corporate = corporate.corporate
        m = form.save(user=request.user, corporate=corporate)
        return redirect(reverse('productList', kwargs={'slug': slug}))
    return render(request, template_name=template, context={'form': form, 'new': True})


@login_required
def ViewProduct(request, slug):
    template = 'settings/products/list.html'
    context = {
        'products': ProductManager().get_corp_products(slug=slug)
    }
    return render(request, template_name=template, context=context)


@login_required
def ViewEditProduct(request, slug):
    template = 'settings/products/details.html'
    product_instance = get_object_or_404(Product, slug=slug)
    form = ProductForm(request.POST or None, slug=slug,
                       instance=product_instance,
                       action=reverse('editProduct', kwargs={'slug': slug}))

    reportForm = BaseReportForm()
    if form.is_valid():
        form.save(user=request.user, corporate=product_instance.corporate)
        return redirect(reverse('productList', kwargs={'slug': product_instance.corporate.slug}))
    return render(request, template_name=template, context={'form': form, 'new': False, 'reportForm': reportForm})


@login_required
def ViewClient(request, slug):
    return None


@login_required
def AddClient(request, slug):
    template = 'clients/details.html'
    form = ClientForm(request.POST or None, slug=slug)
    if form.is_valid():
        corporate = CorpManager().get_corp_form_user_profile(request.user)
        corporate = corporate.corporate
        m = form.save(user=request.user, corporate=corporate)
        return redirect(reverse('productList', kwargs={'slug': slug}))
    return render(request, template_name=template, context={'form': form, 'new': True})
