from django.views.decorators.cache import never_cache
from django.views.decorators.gzip import gzip_page
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from iRep.Serializers import ProductGroupSerializer, ClientSerializer, \
    OrderSerializers, SchedualSerializers, SalesFunnelSerializer, TimeLineSerializers, CheckInOutSerializers, \
    SalesForceTracking, MemberSerializer, TagSerlizers, FormsSerializers, BillBoardSerializers
from iRep.managers.BillBoards import BillBoards
from iRep.managers.Clients import ClientManager
from iRep.managers.Forms import IForm
from iRep.managers.Orders import OrderManager
from iRep.managers.SalesForce import SalesForceManager
from iRep.managers.Schedular import SchedulerManager
from iRep.managers.Visits import VisitsManager
from iRep.models import SalesForce, ProductGroup, Client, Orders, SalesForceSchedual, SalesFunnelStatus, Visits, Tags, \
    Forms
from django.utils.translation import ugettext_lazy as _
import logging
import datetime

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

    if 'sn' not in request.data:
        resp['msg'] = _('Serial number phone')
        return Response(resp)

    try:
        profile = SalesForce.objects.get(user_pin=request.data['user_pin'],
                                         password_pin=request.data['password'],
                                         corp_id__slug=request.data['corp_id'], serial_number=request.data['sn'])

        resp['code'] = 200
        resp['data'] = MemberSerializer(profile, context={'request': request}).data
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

        productCatQS = ProductGroup.objects.prefetch_related().filter(is_active=True, corporate__slug=slug)
        for row in productCatQS:
            resp['data'].append(ProductGroupSerializer(row, context={"request": request}).data)
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
            resp['data'].append(OrderSerializers(raw, context={"request": request}).data)
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

    if 'lng' not in request.data:
        resp['msg'] = _('Longitude  is missed')
        return Response(resp)

    if 'lat' not in request.data:
        resp['msg'] = _('Latitude  is missed')
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
        sales_force=request.data['sales_force'],
        tags=request.data['tags'] if 'tags' in request.data else None, latitude=request.data['lat'],
        longitude=request.data['lng']

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


@gzip_page
@api_view(['POST'])
@parser_classes((JSONParser,))
def addSchedual(request):
    resp = {}
    resp['code'] = 505

    if 'sales_force' not in request.data or not request.data['sales_force']:
        resp['msg'] = _('Missing sales force')
        return Response(resp)

    if 'client' not in request.data or not request.data['client']:
        resp['msg'] = _('Missing client id')
        return Response(resp)

    if 'date' not in request.data or not request.data['date']:
        resp['msg'] = _('Missing date')
        return Response(resp)

    if 'time' not in request.data or not request.data['time']:
        resp['msg'] = _('Missing time')
        return Response(resp)

    if 'is_visit' not in request.data:
        resp['msg'] = _('Missing type')
        return Response(resp)

    record = SchedulerManager().add_scheduler(client_id=request.data['client'],
                                              sales_force_id=request.data['sales_force'],
                                              dates=request.data['date'], times=request.data['time'],
                                              notes=request.data['notes'] if 'notes' in request.data else None,
                                              is_visit=request.data['is_visit'],week='0')

    if record:
        resp['code'] = 200
        resp['data'] = SchedualSerializers(record).data

    else:
        resp['msg'] = _('Error during add schedual , contact system administrator')

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
def SalesForceTimeLineStart(request):
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

    try:
        record = SalesForceManager().AddSalesForceTimeLine(sales_force=request.data['sales_force'],
                                                           timeLineDate=request.data['timeline_date'],
                                                           startTime=request.data['start_time'],
                                                           endTime=None,
                                                           km=0,
                                                           hours=0)
        resp['data'] = TimeLineSerializers(record).data
        resp['code'] = 200

        # add activity
        try:
            lastActivity = SalesForce.objects.get(id=request.data['sales_force'])
            lastActivity.last_activity = datetime.datetime.now()
            lastActivity.save()
        except:
            pass


    except Exception as e:
        logger.debug('Error during add sales force timeline cause ' + str(e))
        resp['msg'] = _('Error during add sales force timeline , please contact system administrator')

    return Response(resp)


@gzip_page
@api_view(['POST'])
@parser_classes((JSONParser,))
def SalesForceTimeLineEnd(request):
    resp = {}
    resp['code'] = 500
    if 'timeline_id' not in request.data:
        resp['msg'] = _('TimelineId missed')
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
        record = SalesForceManager().update_sales_force_timeline(id=request.data['timeline_id'],
                                                                 endTime=request.data['end_time'],
                                                                 km=request.data['km'],
                                                                 hours=request.data['hours'])
        resp['data'] = TimeLineSerializers(record).data
        resp['code'] = 200

    except Exception as e:
        logger.debug('Error during add sales force timeline cause ' + str(e))
        resp['msg'] = _('Error during end sales force timeline , please contact system administrator')

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

    if 'check_in_address' not in request.data:
        resp['msg'] = _('Check in address missed')
        return Response(resp)

    # check visit

    object = SchedulerManager().get_schedular(request.data['sales_force'], request.data['client'],
                                              request.data['check_date'])
    if not object:
        schedual_record = SchedulerManager().add_scheduler(client_id=request.data['client'],
                                                           dates=request.data['check_date'],
                                                           sales_force_id=request.data['sales_force'],
                                                           times=request.data['check_time'],
                                                           notes='not schedual visit',week='0')
        if schedual_record:
            #retrievedDateTime = request.data['check_date'] + ' ' +request.data['check_time']
            #datetime_object = datetime.datetime.strptime(str(retrievedDateTime), '%Y-%m-%d %H:%M')
            visit_record = VisitsManager().add_visit(sales_force=request.data['sales_force'],
                                                     branch=request.data['client'],
                                                     visit_date= request.data['check_date'], notes=None,
                                                     schedualed=False, schedual=schedual_record.pk)
            if visit_record:
                checkInOutRecord = SalesForceManager().CheckIn(sales_force=request.data['sales_force'],
                                                               longtude=request.data['longtude'],
                                                               latitude=request.data['latitude'],
                                                               check_date=request.data['check_date'],
                                                               check_time=request.data['check_time'],
                                                               branch=request.data['client'], visit=visit_record,
                                                               check_in_address=request.data['check_in_address'])
                if checkInOutRecord:
                    resp['code'] = 200
                    resp['data'] = CheckInOutSerializers(checkInOutRecord).data
            else:
                resp['msg'] = _('Error during add non schedual visit , please check with system administrator')

        else:
            resp['msg'] = _('Error during add  schedual  , please check with system administrator')


    else:
        #retrievedDateTime = request.data['check_date'] + ' ' +request.data['check_time']
        #datetime_object = datetime.datetime.strptime(str(retrievedDateTime), '%Y-%m-%d %H:%M')
        visit_record = VisitsManager().add_visit(sales_force=request.data['sales_force'],
                                                 branch=request.data['client'],
                                                 visit_date= request.data['check_date'], notes=None,
                                                 schedualed=True, schedual=object[0].pk)
        if visit_record:
            checkInOutRecord = SalesForceManager().CheckIn(sales_force=request.data['sales_force'],
                                                           longtude=request.data['longtude'],
                                                           latitude=request.data['latitude'],
                                                           check_date=request.data['check_date'],
                                                           check_time=request.data['check_time'],
                                                           branch=request.data['client'], visit=visit_record,check_in_address=request.data['check_in_address'])
            if checkInOutRecord:
                resp['code'] = 200
                resp['data'] = CheckInOutSerializers(checkInOutRecord).data
            else:
                resp['msg'] = _('Error during set check in , please check with system administrator')

        else:
            resp['msg'] = _('Error during add non schedual visit , please check with system administrator')

    return Response(resp)


@gzip_page
@api_view(['POST'])
@parser_classes((JSONParser,))
def CheckOut(request):
    resp = {}
    resp['code'] = 500

    if 'check_date' not in request.data:
        resp['msg'] = _('Check Date missed')
        return Response(resp)

    if 'check_time' not in request.data:
        resp['msg'] = _('Check Time missed')
        return Response(resp)

    if 'check_in_id' not in request.data:
        resp['msg'] = _('Check In ID missed')
        return Response(resp)

    if 'check_out_address' not in request.data:
        resp['msg'] = _('Check out Address  missed')
        return Response(resp)

    record = SalesForceManager().checkOut(id=request.data['id'], check_date=request.data['check_date'],
                                          check_time=request.data['check_time'], check_out_address=request.data['check_out_address'])
    if record:
        resp['code'] = 200
        resp['data'] = CheckInOutSerializers(record).data
    else:
        resp['msg'] = _('Error during set check in , please check with system administrator')

    return Response(resp)


@gzip_page
@api_view(['POST'])
@parser_classes((JSONParser,))
def Track(request):
    resp = {}
    resp['code'] = 500

    if 'sales_force' not in request.data:
        resp['msg'] = _('Sales force missed')
        return Response(resp)

    if 'latitude' not in request.data:
        resp['msg'] = _('Latitude missed')
        return Response(resp)

    if 'longitude' not in request.data:
        resp['msg'] = _('Longitude missed')
        return Response(resp)

    record = SalesForceManager().Tracking(request.data['sales_force'], latitude=request.data['latitude'],
                                          longitude=request.data['longitude'])
    if record:
        resp['code'] = 200
        resp['data'] = SalesForceTracking(record).data
    else:

        resp['msg'] = _('Error during set tracking , please check with system administrator')

    return Response(resp)


@gzip_page
@api_view(['POST'])
@parser_classes((JSONParser,))
def OrderCreate(request):
    resp = {}
    resp['code'] = 500

    if 'sales_force' not in request.data:
        resp['msg'] = _('Sales force missed')
        return Response(resp)

    if 'client_id' not in request.data:
        resp['msg'] = _('Client missed')
        return Response(resp)

    if 'order_date' not in request.data:
        resp['msg'] = _('Order date missed')
        return Response(resp)

    if 'total' not in request.data:
        resp['msg'] = _('Total amount missed')
        return Response(resp)

    if 'sub_total' not in request.data:
        resp['msg'] = _('Subtotal amount missed')
        return Response(resp)

    if 'discount' not in request.data:
        resp['msg'] = _('Discount amount missed')
        return Response(resp)

    if 'items' not in request.data:
        resp['msg'] = _('Order Item missed')
        return Response(resp)

    orderInstance = OrderManager()

    order_instance = orderInstance.save_order(sales_force_id=request.data['sales_force'],
                                              branch_id=request.data['client_id'],
                                              order_date=request.data['order_date'],
                                              total=request.data['total'], sub_total=request.data['sub_total'],
                                              discount=request.data['discount'],
                                              visit_id=request.data['visit_id'] if 'visit_id' in request.data else None,
                                              notes=request.data['notes'] if 'notes' in request.data else None,
                                              items=request.data['items'])
    if order_instance:
        resp['code'] = 200
        resp['data'] = OrderSerializers(order_instance, context={"request": request}).data

    return Response(resp)


@gzip_page
@api_view(['GET'])
def ListTags(request, slug):
    resp = {}
    resp['code'] = 505
    # Validation
    if not slug:
        resp['msg'] = _('Missing corporate')
        return Response(resp)
    try:
        resp['data'] = []
        sqs = Tags.objects.filter(corporate__slug=slug)
        for row in sqs:
            resp['data'].append(TagSerlizers(row).data)
        resp['code'] = 200
    except Exception as e:
        resp['msg'] = _('Can`t retrieve Tags')

    return Response(resp)


@gzip_page
@api_view(['GET'])
def ListForms(request, slug):
    resp = {}
    resp['code'] = 505
    # Validation
    if not slug:
        resp['msg'] = _('Missing corporate')
        return Response(resp)

    try:
        resp['data'] = []
        sqs = Forms.objects.prefetch_related('form_questions').filter(corporate__slug=slug, is_active=True)
        for row in sqs:
            resp['data'].append(FormsSerializers(row).data)
        resp['code'] = 200
    except Exception as e:
        resp['msg'] = _('Can`t retrieve Forms')

    return Response(resp)


@api_view(['POST'])
def QuestionAnswer(request):
    resp = {}
    resp['code'] = 500

    if 'sales_force' not in request.data:
        resp['msg'] = _('Sales force missed')
        return Response(resp)

    if 'answers' not in request.data:
        resp['msg'] = _('Question Answer missed')
        return Response(resp)

    if 'visit_id' not in request.data:
        resp['msg'] = _('Visit id missed')
        return Response(resp)
    
    if 'client' not in request.data:
        resp['msg'] = _('Client id missed')
        return Response(resp)

    iForm = IForm(slug=None)
    for raw in request.data['answers']:
        if 'question_id' not in raw:
            resp['msg'] = _('Question Id missed')
            return Response(resp)

        if 'answer' not in raw:
            resp['msg'] = _('Question answer missed')
            return Response(resp)

        status = iForm.saveFormQuestionAnswer(question_id=raw['question_id'],
                                              sales_force=request.data['sales_force'], answer=raw['answer'],
                                              visit_id=request.data['visit_id'],branch_id=request.data['client'])

        if status:
            resp['data'] = _('Saved')
            resp['code'] = 200
        else:
            resp['data'] = _('Error during saving ')

    return Response(resp)


@api_view(['GET'])
def ListBillboard(request, slug):
    resp = {}
    resp['code'] = 500

    if not slug:
        resp['msg'] = _('Corporate is missing')
        return Response(resp)

    try:
        billBoards = BillBoards(slug=slug).listToday()
        resp['data'] = []
        for row in billBoards:
            resp['data'].append(BillBoardSerializers(row).data)
        resp['code'] = 200
    except Exception as e:
        logger.debug('error during retrieve billboards cause:-' + str(e))
        print str(e)
        resp['data'] = _('Error during retrieve bill boards ')

    return Response(resp)
