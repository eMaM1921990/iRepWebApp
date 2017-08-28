# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse

from iRep.Serializers import ClientSerializer
from iRep.forms import SalesForceForm, SalesForceReportForm, ProductForm, BaseReportForm, ClientForm, QuestionForm, \
    BaseQuestionFormSet
from iRep.managers.Clients import ClientManager
from iRep.managers.Corp import CorpManager
from iRep.managers.Forms import Forms
from iRep.managers.Products import ProductManager
from iRep.managers.Reports import TrackingReports
from iRep.managers.Resources import VisitsResource, SchedualResource, OrderResource
from iRep.managers.SalesForce import SalesForceManager
from iRep.managers.Schedular import SchedulerManager
from iRep.models import SalesForce, Product, Client, Visits, SalesForceSchedual, Orders
from django.utils.translation import ugettext_lazy as _


@login_required
def home(request):
    template = 'index.html'
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
        return redirect(reverse('viewSalesForceByUser', kwargs={'slug': corp.slug}))
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
    reportForm = SalesForceReportForm(sales_force= sales_force_instance.id)
    if form.is_valid():
        form.save(user=request.user)
        return redirect(reverse('viewSalesForceByUser',kwargs={'slug':corp.slug}))
    # Retreve clients
    sqs = ClientManager().get_client_by_sales_force(slug)
    data = []
    # serialize data
    if sqs:
        for row in sqs:
            data.append(ClientSerializer(row).data)
        data = json.dumps(data, ensure_ascii=False)

    # retrieve schedual
    schedular = SchedulerManager().get_schedul_by_sales_force(sales_force=slug)
    return render(request, template_name=template,
                  context={'form': form, 'new': False, 'reportForm': reportForm, 'clients': data, 'sales_force_id':sales_force_instance.pk,'schedular':schedular})


@login_required
def AddProduct(request, slug):
    template = 'settings/products/details.html'
    form = ProductForm(request.POST or None,request.FILES or None, slug=slug, action=reverse('createProduct', kwargs={'slug': slug}))
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
    form = ProductForm(request.POST or None,request.FILES or None, slug=slug,
                       instance=product_instance,
                       action=reverse('editProduct', kwargs={'slug': slug}))

    reportForm = BaseReportForm()
    if form.is_valid():
        form.save(user=request.user, corporate=product_instance.corporate)
        return redirect(reverse('productList', kwargs={'slug': product_instance.corporate.slug}))
    return render(request, template_name=template, context={'form': form, 'new': False, 'reportForm': reportForm})


@login_required
def ViewClient(request, slug):
    template = 'clients/list.html'
    context = {
        'clients': ClientManager().get_client_by_slug(slug=slug)
    }
    return render(request, template_name=template, context=context)


@login_required
def AddClient(request, slug):
    template = 'clients/details.html'
    form = ClientForm(request.POST or None, action=reverse('AddClient', kwargs={'slug': slug}))
    if form.is_valid():
        corporate = CorpManager().get_corp_form_user_profile(request.user)
        corporate = corporate.corporate
        m = form.save(user=request.user, corporate=corporate, main_branch=None)
        return redirect(reverse('viewClient', kwargs={'slug': slug}))
    return render(request, template_name=template, context={'form': form, 'new': True})


@login_required
def EditClient(request, slug):
    template = 'clients/details.html'
    client_instance = get_object_or_404(Client, slug=slug)
    form = ClientForm(request.POST or None, instance=client_instance,
                      action=reverse('EditClient', kwargs={'slug': slug}))
    reportForm = SalesForceReportForm()
    if form.is_valid():
        corporate = CorpManager().get_corp_form_user_profile(request.user)
        corporate = corporate.corporate
        m = form.save(user=request.user, corporate=corporate, main_branch=None)
        return redirect(reverse('viewClient', kwargs={'slug': slug}))

    # retrieve schedual
    schedular = SchedulerManager().get_scheduler_by_client(client_slug=slug)

    return render(request, template_name=template, context={'form': form, 'new': False, 'reportForm': reportForm,'schedular':schedular})


# Export
def ExportVisits(request):
    if request.POST:
        visitResources = VisitsResource()
        if 'fromDate' in request.POST and len(request.POST['fromDate']) > 0:
            sqs = Visits.objects.filter(visit_date__gte=request.POST['fromDate'])
        if 'toDate' in request.POST and len(request.POST['toDate']) > 0:
            sqs = Visits.objects.filter(visit_date__lte=request.POST['toDate'])
        if 'salesForce' in request.POST and len(request.POST['salesForce']) > 0:
            sqs = Visits.objects.filter(sales_force__id=request.POST['toDate'])

        dataset = visitResources.export(sqs)
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="visits.csv"'
        return response


@login_required
def ExportSchedual(request):
    if request.POST:
        schedualResources = SchedualResource()
        if 'fromDate' in request.POST and len(request.POST['fromDate']) > 0:
            sqs = SalesForceSchedual.objects.filter(schedual_date__gte=request.POST['fromDate'])
        if 'toDate' in request.POST and len(request.POST['toDate']) > 0:
            sqs = SalesForceSchedual.objects.filter(schedual_date__lte=request.POST['toDate'])
        if 'salesForce' in request.POST and len(request.POST['salesForce']) > 0:
            sqs = SalesForceSchedual.objects.filter(sales_force__id=request.POST['toDate'])

        dataset = schedualResources.export(sqs)
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="schedual.csv"'
        return response


@login_required
def ExportOrders(request):
    if request.POST:
        orderResources = OrderResource()
        if 'fromDate' in request.POST and len(request.POST['fromDate']) > 0:
            sqs = Orders.objects.filter(order_date__gte=request.POST['fromDate'])
        if 'toDate' in request.POST and len(request.POST['toDate']) > 0:
            sqs = Orders.objects.filter(order_date__lte=request.POST['toDate'])
        if 'salesForce' in request.POST and len(request.POST['salesForce']) > 0:
            sqs = Orders.objects.filter(sales_force__id=request.POST['toDate'])

        dataset = orderResources.export(sqs)
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="schedual.csv"'
        return response


@login_required
def AddScheduler(request):
    if request.POST:
        valid = False
        message = _('Error during save scheduler')
        schedual_instance = SchedulerManager()
        result = schedual_instance.add_scheduler(request.POST['client_id'], request.POST['sales_force_id'], request.POST['dates'],
                                        request.POST['times'], request.POST['notes'])
        if result:
            valid = True
            message =_('Schedual add successfully')

        ret = {
            "valid":valid,
            "msg":message
        }
        return HttpResponse(json.dumps(ret, ensure_ascii=False))

## FROMS
@login_required
def ViewForms(request, slug):
    template = 'forms/list.html'
    context = {
        'formList': Forms.getFormList(slug=slug)
    }
    return render(request, template_name=template, context=context)

def CreateOrEditForms(request,slug):
    # Create the formset, specifying the form and formset we want to use.
    QuestionFormSet = formset_factory(QuestionForm, formset=BaseQuestionFormSet)

    # Get our existing  data for this user.  This is used as initial data.

###################
# REPORTS
####################
@login_required
def TrackingVisitReportByClient(request):
    if request.POST:
        template = 'sales_force/visits_track_rows.html'
        trackingInstance = TrackingReports(start_date=request.POST['id_date_from'],end_date=request.POST['id_date_to'])
        result = trackingInstance.visits_by_client(client_id=request.POST['client_id'])
        ret = {
            "data":result
        }

        return HttpResponse(json.dumps(ret,ensure_ascii=False))

@login_required
def TrackingVisitReportBySalesForce(request):
    if request.POST:
        valid = False
        template = 'sales_force/visit_track_rows.html'
        trackingInstance = TrackingReports(start_date=request.POST['date_from'],end_date=request.POST['date_to'])
        result = trackingInstance.visits_by_sales_force(sales_force_id=request.POST['sales_force'])
        html = None
        if result:
            valid = True
            html = render_to_string(template_name=template,context={'tracking':result})
        ret = {
            "html":html,
            "valid":valid
        }

        return HttpResponse(json.dumps(ret,ensure_ascii=False))