# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
import json

import datetime
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

from iRep.Serializers import ClientSerializer, ProductGroupWithoutProductSerialziers, SalesForceSerializer
from iRep.forms import SalesForceForm, SalesForceReportForm, ProductForm, BaseReportForm, ClientForm, QuestionForm, \
    BaseQuestionFormSet, FormsForm, ProductCategoryForm, BillBoardForm, ClientReportForm
from iRep.managers.AuditRetail import AuditRetail
from iRep.managers.BillBoards import BillBoards
from iRep.managers.Clients import ClientManager
from iRep.managers.Corp import CorpManager
from iRep.managers.Forms import Forms, IForm
from iRep.managers.Orders import OrderManager
from iRep.managers.Products import ProductManager
from iRep.managers.Reports import TrackingReports, DashBoardReports
from iRep.managers.Resources import VisitsResource, SchedualResource, OrderResource, SalesForceResource, ClientResource, \
    FormResource, ProductResource, AuditRetailResources
from iRep.managers.SalesForce import SalesForceManager
from iRep.managers.Schedular import SchedulerManager
from iRep.models import SalesForce, Product, Client, Visits, SalesForceSchedual, Orders, FormQuestions, BillBoard, \
    AuditRetails
from django.utils.translation import ugettext_lazy as _


@login_required
def home(request):
    context = {}
    template = 'index.html'
    # Get Corp Info
    corp = CorpManager().get_corp_by_user(request.user)
    currentDate = datetime.datetime.today().strftime('%Y-%m-%d')
    if request.POST:
        currentDate = request.POST.get('date', currentDate)

    DashBoardReports(currentDate,
                     currentDate, None, corp,
                     context).get_dashboard_statistics()

    context['locations'] = TrackingReports(currentDate
                                           , currentDate
                                           ).tracking_sales_force_by_corp(corp)
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
            data.append(ClientSerializer(row, context={'request': request}).data)
        data = json.dumps(data, ensure_ascii=False)

    # retrieve schedual
    schedular = SchedulerManager().get_schedul_by_sales_force(sales_force=slug)
    return render(request, template_name=template,
                  context={'form': form, 'new': False, 'reportForm': reportForm, 'clients': data,
                           'sales_force_id': sales_force_instance.pk, 'schedular': schedular})


@login_required
def DeleteSalesForce(request, slug):
    corp = CorpManager().get_corp_by_user(request.user)
    SalesForceManager().deleteSalesForce(slug)
    return redirect(reverse('viewSalesForceByUser', kwargs={'slug': corp.slug}))


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
def DeleteProduct(request, slug):
    # Get product
    corp = CorpManager().get_corp_by_user(request.user)
    ProductManager().deleteProduct(slug=slug)
    return redirect(reverse('productList', kwargs={'slug': corp.slug}))


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
    form = ProductForm(request.POST or None, request.FILES or None, slug=product_instance.corporate.slug,
                       instance=product_instance,
                       action=reverse('editProduct', kwargs={'slug': slug}))

    categoryForm = ProductCategoryForm(request.POST or None)

    reportForm = BaseReportForm()
    if form.is_valid():
        corporate = CorpManager().get_corp_form_user_profile(request.user)
        corporate = corporate.corporate
        form.save(user=request.user, corporate=corporate)
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
    # Get Corp Info
    corp = CorpManager().get_corp_by_user(request.user)
    form = ClientForm(request.POST or None, action=reverse('AddClient', kwargs={'slug': slug}), corp_instance=corp)
    if form.is_valid():
        corporate = CorpManager().get_corp_form_user_profile(request.user)
        corporate = corporate.corporate
        m = form.save(user=request.user, corporate=corporate, main_branch=None)
        return redirect(reverse('viewClient', kwargs={'slug': slug}))
    return render(request, template_name=template, context={'form': form, 'new': True})


@login_required
def DeleteClient(request, slug):
    corp = CorpManager().get_corp_by_user(request.user)
    ClientManager().deleteClient(slug)
    return redirect(reverse('viewClient', kwargs={'slug': corp.slug}))


@login_required
def viewOrder(request, slug):
    template = 'orders/details.html'
    orders = OrderManager().get_corp_orders(slug=slug)
    return render(request, template_name=template, context={'orders': orders})


@login_required
def EditClient(request, slug):
    template = 'clients/details.html'
    # Get Corp Info
    corp = CorpManager().get_corp_by_user(request.user)
    client_instance = get_object_or_404(Client, slug=slug)
    form = ClientForm(request.POST or None, instance=client_instance, corp_instance=corp,
                      action=reverse('EditClient', kwargs={'slug': slug}))
    reportForm = ClientReportForm(client=client_instance.id)
    if form.is_valid():
        corporate = CorpManager().get_corp_form_user_profile(request.user)
        corporate = corporate.corporate
        m = form.save(user=request.user, corporate=corporate, main_branch=None)
        return redirect(reverse('viewClient', kwargs={'slug': corp.slug}))

    # retrieve schedual
    schedular = SchedulerManager().get_scheduler_by_client(client_slug=slug)

    # retrieve client salesforce
    sqs = ClientManager().get_sales_force_by_client(slug=slug)
    data = []
    # serialize data
    if sqs:
        for row in sqs:
            data.append(SalesForceSerializer(row, context={'request': request}).data)
        data = json.dumps(data, ensure_ascii=False)

    return render(request, template_name=template,
                  context={'form': form, 'new': False, 'reportForm': reportForm, 'schedular': schedular,
                           'sales_force': data, 'client_id': client_instance.pk})


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
    sqs = Orders.objects
    orderResources = OrderResource()
    if request.POST:
        if 'fromDate' in request.POST and len(request.POST['fromDate']) > 0:
            sqs = sqs.filter(order_date__gte=request.POST['fromDate'])
        if 'toDate' in request.POST and len(request.POST['toDate']) > 0:
            sqs = sqs.filter(order_date__lte=request.POST['toDate'])
        if 'salesForce' in request.POST and len(request.POST['salesForce']) > 0:
            sqs = sqs.filter(sales_force__id=request.POST['toDate'])

    # Get Corp Info
    corp = CorpManager().get_corp_by_user(request.user)
    sqs = sqs.filter(branch__corporate=corp)
    dataset = orderResources.export(sqs)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'
    return response


@login_required
def ExportSalesForce(request):
    salesForceResources = SalesForceResource()
    # Get Corp Info
    corp = CorpManager().get_corp_by_user(request.user)
    sqs = SalesForce.objects.filter(corp_id=corp)
    dataset = salesForceResources.export(sqs)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_force.csv"'
    return response


@login_required
def ExportClients(request):
    clientResources = ClientResource()
    # Get Corp Info
    corp = CorpManager().get_corp_by_user(request.user)
    sqs = Client.objects.filter(corporate=corp)
    dataset = clientResources.export(sqs)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clients.csv"'
    return response


@login_required
def ExportForms(request):
    resource = FormResource()
    # Get Corp Info
    corp = CorpManager().get_corp_by_user(request.user)
    sqs = Forms.objects.filter(corporate=corp)
    dataset = resource.export(sqs)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="forms.csv"'
    return response


@login_required
def ExportProduct(request):
    resource = ProductResource()
    # Get Corp Info
    corp = CorpManager().get_corp_by_user(request.user)
    sqs = Product.objects.filter(corporate=corp)
    dataset = resource.export(sqs)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="product.csv"'
    return response


@login_required
def ExportAuditRetails(request):
    resource = AuditRetailResources()
    # Get Corp Info
    corp = CorpManager().get_corp_by_user(request.user)
    sqs = AuditRetails.objects.filter(corporate=corp)
    dataset = resource.export(sqs)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="auditRetails.csv"'
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
def ViewFormQuestionAnswer(request):
    valid = False
    template = 'forms/form_answer.html'
    answerList = IForm(slug=None).getFormQuestionAnswer(id=request.POST['id'], branch=request.POST['branch_id'])
    if answerList:
        valid = True
        html = render_to_string(template, {'answerList': answerList})

    ret = {
        'valid': valid,
        'html': html

    }
    return HttpResponse(json.dumps(ret, ensure_ascii=False))


@login_required
def exportForm(request, id):
    visit_id = id
    # Form
    formInfo = IForm(slug=None).getFormQuestionAnswerVisit(visit_id=visit_id)
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    if formInfo:
        response['Content-Disposition'] = 'attachment; filename="' + visit_id + '.csv"'
    else:
        response['Content-Disposition'] = 'attachment; filename="visit_form.csv"'

    writer = csv.writer(response)
    field_names = ["Question ", "Answer"]
    writer.writerow(field_names)
    for question in formInfo:
        writer.writerow([question.question.question, question.answer])

    return response


@login_required
def DeleteForm(request, id):
    # Get Corp Info
    corp = CorpManager().get_corp_by_user(request.user)
    IForm(slug=None).deleteForm(id)
    return redirect(reverse('ViewForms', kwargs={'slug': corp.slug}))


@login_required
def CreateForms(request, slug):
    # Get Corp Info
    corp = CorpManager().get_corp_by_user(request.user)

    template = 'forms/form.html'
    # Create the formset, specifying the form and formset we want to use.
    QuestionFormSet = formset_factory(QuestionForm, formset=BaseQuestionFormSet)
    formsForm = FormsForm(request.POST or None, user=request.user, corp=corp)

    QuestionFormSetform = QuestionFormSet(request.POST or None)

    if formsForm.is_valid():
        m = formsForm.save()

        # Now save the data for each form in the formset
        new_questions = []
        for question_form in QuestionFormSetform:
            print question_form
            new_questions.append(FormQuestions(form=m, question=question_form.cleaned_data.get('question')))

        try:
            with transaction.atomic():
                # Replace the old with the new
                FormQuestions.objects.filter(form=m).delete()
                FormQuestions.objects.bulk_create(new_questions)

                # And notify our users that it worked
                messages.success(request, 'You have updated your form.')
                # Redirect
                return redirect(reverse('ViewForms', kwargs={'slug': slug}))

        except IntegrityError:  # If the transaction failed
            messages.error(request, 'There was an error saving your form.')

    context = {
        'formsForm': formsForm,
        'QuestionFormSetform': QuestionFormSetform,
    }

    return render(request, template, context)


@login_required
def EditForms(request, slug, id):
    # Get Corp Info
    corp = CorpManager().get_corp_by_user(request.user)

    template = 'forms/form.html'
    # Create the formset, specifying the form and formset we want to use.
    QuestionFormSet = formset_factory(QuestionForm, formset=BaseQuestionFormSet)

    # Get our existing  data for this user.  This is used as initial data.
    question_data = None
    form_questions = IForm(slug=slug).getFormQuestions(id)
    if form_questions:
        question_data = [{'question': l.question}
                         for l in form_questions]

    formsForm = FormsForm(request.POST or None, user=request.user, corp=corp, instance=IForm(slug).getFormInfo(id=id))

    QuestionFormSetform = QuestionFormSet(request.POST or None, initial=question_data)

    if formsForm.is_valid():
        m = formsForm.save()

        # Now save the data for each form in the formset
        new_questions = []
        for question_form in QuestionFormSetform:
            print hasattr(question_form, 'cleaned_data')
            print question_form
            new_questions.append(FormQuestions(form=m, question=question_form.cleaned_data.get('question')))

        try:
            with transaction.atomic():
                # Replace the old with the new
                FormQuestions.objects.filter(form=m).delete()
                FormQuestions.objects.bulk_create(new_questions)

                # And notify our users that it worked
                messages.success(request, 'You have updated your form.')

                # Redirect
                return redirect(reverse('ViewForms', kwargs={'slug': slug}))

        except IntegrityError:  # If the transaction failed
            messages.error(request, 'There was an error saving your form.')
            return redirect(reverse('ViewForms', kwargs={'slug': slug}))

    context = {
        'formsForm': formsForm,
        'QuestionFormSetform': QuestionFormSetform,
        'edit': True,
        'id': id
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
        template2 = 'sales_force/visit_track_rows2.html'
        trackingInstance = TrackingReports(start_date=request.POST['date_from'], end_date=request.POST['date_to'])
        result = trackingInstance.visits_by_sales_force(sales_force_id=request.POST['sales_force'])
        totalVisits = trackingInstance.countTotalPlaceVisited(sales_force_id=request.POST['sales_force'])
        totalOrder = trackingInstance.countNumberOfOrders(sales_force_id=request.POST['sales_force'])
        totalVisitGroupByBranch = trackingInstance.countTotalPlaceVisitedGroupByBranch(
            sales_force_id=request.POST['sales_force'])
        totalHrAndMile = trackingInstance.countSalesForceTimeAndMile(sales_force_id=request.POST['sales_force'])
        totalTimeInPlace = trackingInstance.countTimeinPlace(sales_force_id=request.POST['sales_force'])
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
        html2 = None
        if result:
            valid = True
            html = render_to_string(template_name=template, context={'tracking': result})
            html2 = render_to_string(template_name=template2, context={'tracking': result})
        ret = {
            "html": html,
            "html2": html2,
            "valid": valid,
            "totalVisits": totalVisits,
            "totalOrder": totalOrder,
            "totalVisitGroupByBranch":totalVisitGroupByBranch,
            "hr": hr,
            "km": km,
            "countDay": countDay,
            "totalTimePlace": str(totalTimeInPlace[0]['totalTime']) if totalTimeInPlace else None

        }

        return HttpResponse(json.dumps(ret, ensure_ascii=False))


# Bill boards
@login_required
def billBoards(request, slug):
    template = 'settings/billBoard/list.html'
    context = {
        'billBoards': BillBoards(slug=slug).list()
    }
    return render(request, template_name=template, context=context)


@login_required
def newBillBoard(request):
    template = 'settings/billBoard/form.html'

    # Get Corp Info
    corp = CorpManager().get_corp_by_user(request.user)

    form = BillBoardForm(request.POST or None, action=reverse('newBillBoards'))
    if form.is_valid():
        m = form.save(user=request.user, corporte=corp)
        if m:
            return redirect(reverse('billBoards', kwargs={'slug': corp.slug}))
    context = {
        'form': form
    }
    return render(request, template_name=template, context=context)


@login_required
def editBillBoard(request, id):
    template = 'settings/billBoard/form.html'

    # Get Corp Info
    corp = CorpManager().get_corp_by_user(request.user)

    # Bill boards
    instance = get_object_or_404(BillBoard, id=id)

    form = BillBoardForm(request.POST or None, instance=instance, action=reverse('editBillBoard', kwargs={'id': id}))
    if form.is_valid():
        m = form.save(user=request.user, corporte=corp)
        if m:
            return redirect(reverse('billBoards', kwargs={'slug': corp.slug}))
    context = {
        'form': form
    }
    return render(request, template_name=template, context=context)


@login_required
def auditRetails(request, slug):
    template = 'settings/auditRetail/list.html'
    context = {
        'auditRetails': AuditRetail(slug).getAuditRetails()
    }

    return render(request, template_name=template, context=context)


@login_required
def dashboard(request, slug):
    template = 'clients/dashboard.html'
    context = {}

    if request.POST:
        # Get Corp Info
        corp = CorpManager().get_corp_by_user(request.user)
        dashboards = DashBoardReports(start_date=request.POST['dateFrom'], end_date=request.POST['dateTo'], city=None,
                                      corp=corp, context=None)
        context['visitDetails'] = dashboards.get_visit_details_charts()
        context['orders'] = dashboards.get_total_orders_chart()
    return render(request, template_name=template, context=context)


@login_required
def ClientReport(request):
    if request.POST:
        trackingInstance = TrackingReports(start_date=request.POST['date_from'], end_date=request.POST['date_to'])
        visitCount = trackingInstance.visits_by_client_count(client_id=request.POST['client_id'])
        orders = trackingInstance.countNumberOfOrdersByClient(client_id=request.POST['client_id'])

        ret = {
            'visits': visitCount,
            'orders': orders
        }

        return HttpResponse(json.dumps(ret, ensure_ascii=False))
