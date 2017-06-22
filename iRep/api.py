from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.decorators.gzip import gzip_page
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from iRep.Serializers import SalesForceSerializer, ProductSerializer, ProductGroupSerializer, ClientSerializer, \
    OrderSerializers, SchedualSerializers, SalesFunnelSerializer, TimeLineSerializers, CheckInOutSerializers
from iRep.managers.Clients import ClientManager
from iRep.managers.SalesForce import SalesForceManager
from iRep.managers.Schedular import SchedulerManager
from iRep.managers.Visits import VisitsManager
from iRep.models import SalesForce, ProductGroup, Client, Orders, SalesForceSchedual, SalesFunnelStatus, Visits
from django.utils.translation import ugettext_lazy as _
import logging

logger = logging.getLogger(__name__)


@gzip_page
@never_cache
@api_view(['POST'])
@parser_classes((JSONParser,))
def SalesForceLogin(request):
    resp = {}
    resp['code'] = 505
    # validations
    if 'user_pin' not in request.data:
        resp['msg'] = _('Missing user pin.')
        return Response(resp)

    if 'password' not in request.data:
        resp['msg'] = _('Missing password')
        return Response(resp)

    if 'corp_id' not in request.data:
        resp['msg'] = _('Missing corpId')
        return Response(resp)

    try:
        profile = SalesForce.objects.get(user_pin=request.data['user_pin'],
                                         password_pin=request.data['password'],
                                         corp_id__slug=request.data['corp_id'])

        resp['code'] = 200
        resp['data'] = SalesForceSerializer(profile, context={'request': request}).data
        return Response(resp)

    except Exception as e:
        print str(e)
        logger.debug('Error during login for ' + str(request.data) + ' cause: ' + str(e))
        resp['msg'] = _('Invalid login credentials info ')
        return Response(resp)


@gzip_page
@api_view(['GET'])
def ProductCategory(request, slug):
    resp = {}
    resp['code'] = 505
    # Validation
    if not slug:
        resp['msg'] = _('Missing corpID')
        return Response(resp)

    try:
        resp['data'] = []

        productCatQS = ProductGroup.objects.filter(is_active=True, corporate__slug=slug)
        for row in productCatQS:
            resp['data'].append(ProductGroupSerializer(row).data)
        resp['code'] = 200

    except Exception as e:
        print str(e)
        resp['msg'] = _('Can`t retrieve product catalog')

    return Response(resp)


@gzip_page
@api_view(['GET'])
def Clients(request, slug):
    resp = {}
    resp['code'] = 505
    # Validation
    if not slug:
        resp['msg'] = _('Missing corpID')
        return Response(resp)
    try:
        resp['data'] = []
        ClientQS = Client.objects.filter(is_active=True, sales_force__slug=slug)
        for row in ClientQS:
            resp['data'].append(ClientSerializer(row).data)
        resp['code'] = 200

    except Exception as e:
        print str(e)
        resp['msg'] = _('Can`t retrieve clients')

    return Response(resp)


@gzip_page
@api_view(['GET'])
def ClientsOrder(request, clientId):
    resp = {}
    resp['code'] = 505
    # Validation
    if not clientId:
        resp['msg'] = _('Missing Client ID')
        return Response(resp)
    try:

        resp['data'] = []
        ordersQS = Orders.objects.filter(branch__id=clientId)
        for raw in ordersQS:
            resp['data'].append(OrderSerializers(raw).data)
        resp['code'] = 200
    except Exception as e:
        resp['msg'] = _('Can`t retrieve client orders')

    return Response(resp)


@gzip_page
@api_view(['POST'])
@parser_classes((JSONParser,))
def AddClient(request):
    resp = {}
    resp['code'] = 505
    # validations
    if 'name' not in request.data:
        resp['msg'] = _('Name is missed')
        return Response(resp)

    if 'address_txt' not in request.data:
        resp['msg'] = _('Address is missed')
        return Response(resp)

    if 'zipcode' not in request.data:
        resp['msg'] = _('Zipcode is missed')
        return Response(resp)

    if 'contact_name' not in request.data:
        resp['msg'] = _('Contact name is missed')
        return Response(resp)

    if 'contact_title' not in request.data:
        resp['msg'] = _('Contact title is missed')
        return Response(resp)

    if 'website' not in request.data:
        resp['msg'] = _('Website is missed')
        return Response(resp)

    if 'email' not in request.data:
        resp['msg'] = _('Email is missed')
        return Response(resp)

    if 'phone' not in request.data:
        resp['msg'] = _('Phone is missed')
        return Response(resp)

    if 'notes' not in request.data:
        resp['msg'] = _('Notes is missed')
        return Response(resp)

    if 'corporate' not in request.data:
        resp['msg'] = _('Corporate is missed')
        return Response(resp)

    if 'status' not in request.data:
        resp['msg'] = _('Client  is missed')
        return Response(resp)

    if 'city' not in request.data:
        resp['msg'] = _('City  is missed')
        return Response(resp)

    if 'state' not in request.data:
        resp['msg'] = _('State  is missed')
        return Response(resp)

    if 'country' not in request.data:
        resp['msg'] = _('Country  is missed')
        return Response(resp)

    if 'sales_force' not in request.data:
        resp['msg'] = _('Sales force  is missed')
        return Response(resp)

    status = ClientManager().CreateClientFromAPI(
        name=request.data['name'],
        address_txt=request.data['address_txt'],
        zipcode=request.data['zipcode'],
        contact_name=request.data['contact_name'],
        contact_title=request.data['contact_title'],
        website=request.data['website'],
        email=request.data['email'],
        phone=request.data['phone'],
        notes=request.data['notes'],
        corporate=request.data['corporate'],
        status=request.data['status'],
        city=request.data['city'],
        state=request.data['state'],
        country=request.data['country'],
        sales_force=request.data['sales_force']

    )

    if not status:
        resp['msg'] = _('Error during add new client ,please check system administator')
        return Response(resp)

    resp['code'] = 200
    resp['data'] = ClientSerializer(status).data
    return Response(resp)


@gzip_page
@api_view(['GET'])
def ListSchedualerBySF(request, sales_force_id):
    resp = {}
    resp['code'] = 505
    # Validation
    if not sales_force_id:
        resp['msg'] = _('Missing sales force')
        return Response(resp)
    try:
        resp['data'] = []
        sqs = SalesForceSchedual.objects.filter(sales_force__id=sales_force_id)
        for row in sqs:
            resp['data'].append(SchedualSerializers(row).data)
        resp['code'] = 200
    except Exception as e:
        resp['msg'] = _('Can`t retrieve clients')

    return Response(resp)


@gzip_page
@api_view(['GET'])
def ListSchedualerByCL(request, client_id):
    resp = {}
    resp['code'] = 505
    # Validation
    if not client_id:
        resp['msg'] = _('Missing client id')
        return Response(resp)
    try:
        resp['data'] = []
        sqs = SalesForceSchedual.objects.filter(branch__id=client_id)
        for row in sqs:
            resp['data'].append(SchedualSerializers(row).data)
        resp['code'] = 200
    except Exception as e:
        resp['msg'] = _('Can`t retrieve clients')

    return Response(resp)


@api_view(['GET'])
@gzip_page
def GetSalesFunnel(request):
    resp = {}
    resp['code'] = 505
    try:
        resp['data'] = []
        sqs = SalesFunnelStatus.objects.all()
        for row in sqs:
            resp['data'].append(SalesFunnelSerializer(row).data)
        resp['code'] = 200
    except Exception as e:
        logger.debug('Error during retrieve sales funnel')

    return Response(resp)


@gzip_page
@api_view(['POST'])
@parser_classes((JSONParser,))
def SalesForceTimeLine(request):
    resp = {}
    resp['code'] = 500
    if 'sales_force' not in request.data:
        resp['msg'] = _('Sales force missed')
        return Response(resp)

    if 'timeline_date' not in request.data:
        resp['msg'] = _('TimeLine date missed')
        return Response(resp)

    if 'start_time' not in request.data:
        resp['msg'] = _('TimeLine start time missed')
        return Response(resp)

    if 'end_time' not in request.data:
        resp['msg'] = _('TimeLine end time missed')
        return Response(resp)

    if 'km' not in request.data:
        resp['msg'] = _('Km missed')
        return Response(resp)

    if 'hours' not in request.data:
        resp['msg'] = _('Total hours missed')
        return Response(resp)

    try:
        record = SalesForceManager().AddSalesForceTimeLine(sales_force=request.data['sales_force'],
                                                           timeLineDate=request.data['timeline_date'],
                                                           startTime=request.data['start_time'],
                                                           endTime=request.data['end_time'],
                                                           km=request.data['km'],
                                                           hours=request.data['hours'])
        resp['data'] = TimeLineSerializers(record).data
        resp['code'] = 200

    except Exception as e:
        logger.debug('Error during add sales force timeline cause ' + str(e))
        resp['msg'] = _('Error during add sales force timeline , please contact system administrator')

    return Response(resp)


@gzip_page
@api_view(['POST'])
@parser_classes((JSONParser,))
def CheckIn(request):
    resp = {}
    resp['code'] = 500

    if 'sales_force' not in request.data:
        resp['msg'] = _('Sales force missed')
        return Response(resp)

    if 'latitude' not in request.data:
        resp['msg'] = _('Latitude missed')
        return Response(resp)

    if 'longtude' not in request.data:
        resp['msg'] = _('Longitude missed')
        return Response(resp)

    if 'check_date' not in request.data:
        resp['msg'] = _('Check Date missed')
        return Response(resp)

    if 'check_time' not in request.data:
        resp['msg'] = _('Check Time missed')
        return Response(resp)

    if 'client' not in request.data:
        resp['msg'] = _('Client missed')
        return Response(resp)

    # check visit

    object = SchedulerManager().get_schedular(request.data['sales_force'], request.data['client'],
                                              request.data['check_date'])
    if not object:
        schedual_record = SchedulerManager().add_scheduler(client_id=request.data['client'],
                                                           dates=request.data['check_date'],
                                                           sales_force_id=request.data['sales_force'],
                                                           times=request.data['check_time'],
                                                           notes='not schedual visit')
        if schedual_record:
            visit_record = VisitsManager().add_visit(sales_force=request.data['sales_force'],
                                                     branch=request.data['client'],
                                                     visit_date=request.data['check_date'], notes=None,
                                                     schedualed=False, schedual=schedual_record)
            if visit_record:
                checkInOutRecord = SalesForceManager().CheckInOut(sales_force=request.data['sales_force'],
                                                                  longtude=request.data['longtude'],
                                                                  latitude=request.data['latitude'],
                                                                  check_date=request.data['check_date'],
                                                                  check_time=request.data['check_time'],
                                                                  branch=request.data['client'], visit=visit_record)
                if checkInOutRecord:
                    resp['code'] = 200
                    resp['data'] = CheckInOutSerializers(checkInOutRecord).data
            else:
                resp['msg'] = _('Error during add non schedual visit , please check with system administrator')

        else:
            resp['msg'] = _('Error during add  schedual  , please check with system administrator')


    else:
        visit_record = VisitsManager().add_visit(sales_force=request.data['sales_force'],
                                                 branch=request.data['client'],
                                                 visit_date=request.data['check_date'], notes=None,
                                                 schedualed=True, schedual=object[0].pk)
        if visit_record:
            checkInOutRecord = SalesForceManager().CheckInOut(sales_force=request.data['sales_force'],
                                                              longtude=request.data['longtude'],
                                                              latitude=request.data['latitude'],
                                                              check_date=request.data['check_date'],
                                                              check_time=request.data['check_time'],
                                                              branch=request.data['client'], visit=visit_record)
            if checkInOutRecord:
                resp['code'] = 200
                resp['data'] = CheckInOutSerializers(checkInOutRecord).data

        else:
            resp['msg'] = _('Error during add non schedual visit , please check with system administrator')

    return Response(resp)
