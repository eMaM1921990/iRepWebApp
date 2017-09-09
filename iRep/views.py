# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db import transaction
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse

from iRep.Serializers import ClientSerializer, ProductGroupWithoutProductSerialziers
from iRep.forms import SalesForceForm, SalesForceReportForm, ProductForm, BaseReportForm, ClientForm, QuestionForm, \
    BaseQuestionFormSet, FormsForm, ProductCategoryForm
from iRep.managers.Clients import ClientManager
from iRep.managers.Corp import CorpManager
from iRep.managers.Forms import Forms, IForm
from iRep.managers.Products import ProductManager
from iRep.managers.Reports import TrackingReports
from iRep.managers.Resources import VisitsResource, SchedualResource, OrderResource
from iRep.managers.SalesForce import SalesForceManager
from iRep.managers.Schedular import SchedulerManager
from iRep.models import SalesForce, Product, Client, Visits, SalesForceSchedual, Orders, FormQuestions
from django.utils.translation import ugettext_lazy as _


@login_required
def home(request):
    context = {}
    template = 'index.html'
    # Get Corp Info
    corp = CorpManager().get_corp_by_user(request.user)
    context['locations'] = TrackingReports(None,None).tracking_sales_force_by_corp(corp)
    return render(request, template_name=template, context=context)


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
    reportForm = SalesForceReportForm(sales_force=sales_force_instance.id)
    if form.is_valid():
        form.save(user=request.user)
        return redirect(reverse('viewSalesForceByUser', kwargs={'slug': corp.slug}))
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
                  context={'form': form, 'new': False, 'reportForm': reportForm, 'clients': data,
                           'sales_force_id': sales_force_instance.pk, 'schedular': schedular})


@login_required
def AddProduct(request, slug):
    template = 'settings/products/details.html'
    form = ProductForm(request.POST or None, request.FILES or None, slug=slug,
                       action=reverse('createProduct', kwargs={'slug': slug}))

    categoryForm = ProductCategoryForm(request.POST or None)
    if form.is_valid():
        corporate = CorpManager().get_corp_form_user_profile(request.user)
        corporate = corporate.corporate
        m = form.save(user=request.user, corporate=corporate)
        return redirect(reverse('productList', kwargs={'slug': slug}))
    return render(request, template_name=template, context={'form': form, 'new': True, 'categoryForm': categoryForm})


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
    form = ProductForm(request.POST or None, request.FILES or None, slug=slug,
                       instance=product_instance,
                       action=reverse('editProduct', kwargs={'slug': slug}))

    categoryForm = ProductCategoryForm(request.POST or None)

    reportForm = BaseReportForm()
    if form.is_valid():
        form.save(user=request.user, corporate=product_instance.corporate)
        return redirect(reverse('productList', kwargs={'slug': product_instance.corporate.slug}))

    return render(request, template_name=template,
                  context={'form': form, 'new': False, 'reportForm': reportForm, 'categoryForm': categoryForm})


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

    return render(request, template_name=template,
                  context={'form': form, 'new': False, 'reportForm': reportForm, 'schedular': schedular})


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
        message = 'Error during save scheduler'
        schedual_instance = SchedulerManager()
        result = schedual_instance.add_scheduler(request.POST['client_id'], request.POST['sales_force_id'],
                                                 request.POST['dates'],
                                                 request.POST['times'], request.POST['notes'])
        if result:
            valid = True
            message = 'Scheduler add successfully'

        ret = {
            "valid": valid,
            "msg": message
        }
        return HttpResponse(json.dumps(ret, ensure_ascii=False))


# product category
@login_required
def AddCategory(request):
    if request.POST:
        valid = False
        user = request.user
        categoryForm = ProductCategoryForm(request.POST or None)
        if categoryForm.is_valid():
            corporate = CorpManager().get_corp_by_user(request.user)
            result = categoryForm.save(user=user, corporate=corporate)
            if result:
                valid = True
                objects = ProductGroupWithoutProductSerialziers(result).data

        ret = {
            "valid": valid,
            "objects": objects
        }
        return HttpResponse(json.dumps(ret, ensure_ascii=False))


## FROMS
@login_required
def ViewForms(request, slug):
    template = 'forms/list.html'
    context = {
        'formList': IForm(slug=slug).getFormList()
    }
    return render(request, template_name=template, context=context)


@login_required
def CreateOrEditForms(request, slug, id=None):
    template = 'forms/form.html'
    # Create the formset, specifying the form and formset we want to use.
    QuestionFormSet = formset_factory(QuestionForm, formset=BaseQuestionFormSet)

    # Get our existing  data for this user.  This is used as initial data.
    form_questions = IForm(slug=slug).getFormQuestions(id)
    if form_questions:
        question_data = [{'question': l.question}
                         for l in form_questions]

    formsForm = FormsForm(request.POST or None, user=request.user)
    QuestionFormSetform = QuestionFormSet(request.POST or None, initial=form_questions)

    if formsForm.is_valid():
        m = formsForm.save()

        # Now save the data for each form in the formset
        new_questions = []
        for question_form in QuestionFormSetform:
            new_questions.append(FormQuestions(form=m, question=question_form.cleaned_data.get('question')))

        try:
            with transaction.atomic():
                # Replace the old with the new
                FormQuestions.objects.filter(form__id=id).delete()
                FormQuestions.objects.bulk_create(new_questions)

                # And notify our users that it worked
                messages.success(request, 'You have updated your form.')

        except IntegrityError:  # If the transaction failed
            messages.error(request, 'There was an error saving your form.')

    context = {
        'formsForm': formsForm,
        'QuestionFormSetform': QuestionFormSetform,
    }

    return render(request, template, context)


###################
# REPORTS
####################
@login_required
def TrackingVisitReportByClient(request):
    if request.POST:
        template = 'sales_force/visits_track_rows.html'
        trackingInstance = TrackingReports(start_date=request.POST['id_date_from'], end_date=request.POST['id_date_to'])
        result = trackingInstance.visits_by_client(client_id=request.POST['client_id'])
        ret = {
            "data": result
        }

        return HttpResponse(json.dumps(ret, ensure_ascii=False))


@login_required
def TrackingVisitReportBySalesForce(request):
    if request.POST:
        valid = False
        template = 'sales_force/visit_track_rows.html'
        trackingInstance = TrackingReports(start_date=request.POST['date_from'], end_date=request.POST['date_to'])
        result = trackingInstance.visits_by_sales_force(sales_force_id=request.POST['sales_force'])
        totalVisits = trackingInstance.countTotalPlaceVisited(sales_force_id=request.POST['sales_force'])
        totalOrder = trackingInstance.countNumberOfOrders(sales_force_id=request.POST['sales_force'])
        totalVisitGroupByBranch = trackingInstance.countTotalPlaceVisitedGroupByBranch(
            sales_force_id=request.POST['sales_force'])
        totalHrAndMile = trackingInstance.countSalesForceTimeAndMile(sales_force_id=request.POST['sales_force'])
        totalTimeInPlace= trackingInstance.countTimeinPlace(sales_force_id=request.POST['sales_force'])
        if not totalVisitGroupByBranch:
            totalVisitGroupByBranch = 0

        if not totalHrAndMile:
            hr = 0
            km = 0
            countDay = 0
        else:
            hr = float(totalHrAndMile[0]['totalHr'])
            km = float(totalHrAndMile[0]['totalKm'])
            countDay = totalHrAndMile[0]['totalDay']

        html = None
        if result:
            valid = True
            html = render_to_string(template_name=template, context={'tracking': result})
        ret = {
            "html": html,
            "valid": valid,
            "totalVisits": totalVisits,
            "totalOrder": totalOrder,
            "totalVisitGroupByBranch": totalVisitGroupByBranch[0]['totalVistitBranch'],
            "hr": hr,
            "km": km,
            "countDay":countDay,
            "totalTimePlace":str(totalTimeInPlace[0]['totalTime'])

        }

        return HttpResponse(json.dumps(ret, ensure_ascii=False))
