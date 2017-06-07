from django.views.decorators.cache import never_cache
from django.views.decorators.gzip import gzip_page
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from iRep.Serializers import SalesForceSerializer, ProductSerializer, ProductGroupSerializer, ClientSerializer, \
    OrderSerializers
from iRep.models import SalesForce, ProductGroup, Client, Orders
from django.utils.translation import ugettext_lazy as _


@gzip_page
@never_cache
@api_view(['POST'])
@parser_classes((JSONParser,))
def SalesForceLogin(request):
    resp = {}
    resp['code'] = None
    # validations
    if 'user_pin' not in request.data:
        resp['code'] = None
        resp['msg'] = _('Missing user pin.')
        return Response(resp)

    if 'password' not in request.data:
        resp['code'] = None
        resp['msg'] = _('Missing password')
        return Response(resp)

    if 'corp_id' not in request.data:
        resp['code'] = None
        resp['msg'] = _('Missing corpId')
        return Response(resp)

    try:
        profile = SalesForce.objects.get(user_pin=request.data['user_pin'],
                                         password_pin=request.data['password'],
                                         corp_id=request.data['corp_id'])

        resp['data'] = SalesForceSerializer(profile, context={'request': request}).data
        return Response(resp)

    except Exception as e:
        print str(e)
        resp['code'] = None
        resp['msg'] = _('Invalid login credentials info ')
        return Response(resp)


@gzip_page
@api_view(['GET'])
def ProductCategory(request, corp_id):
    resp = {}
    resp['code'] = None
    # Validation
    if not corp_id:
        resp['code'] = None
        resp['msg'] = _('Missing corpID')
        return Response(resp)

    try:
        resp['data'] = []
        resp['code'] = None
        productCatQS = ProductGroup.objects.filter(is_active=True, corporate__id=corp_id)
        for row in productCatQS:
            resp['data'].append(ProductGroupSerializer(row).data)

    except Exception as e:
        print str(e)
        resp['code'] = None
        resp['msg'] = _('Can`t retrieve product catalog')

    return Response(resp)


@gzip_page
@api_view(['GET'])
def Clients(request, corpId):
    resp = {}
    resp['code'] = None
    # Validation
    if not corpId:
        resp['code'] = None
        resp['msg'] = _('Missing corpID')
        return Response(resp)
    try:
        resp['data'] = []
        resp['code'] = None
        ClientQS = Client.objects.filter(is_active=True, corporate__id=corpId)
        for row in ClientQS:
            resp['data'].append(ClientSerializer(row).data)

    except Exception as e:
        resp['code'] = None
        resp['msg'] = _('Can`t retrieve clients')

    return Response(resp)


@gzip_page
@api_view(['GET'])
def ClientsOrder(request, clientId):
    resp = {}
    resp['code'] = None
    # Validation
    if not clientId:
        resp['code'] = None
        resp['msg'] = _('Missing Client ID')
        return Response(resp)
    try:
        resp['code'] = None
        resp['data'] = []
        ordersQS = Orders.objects.filter(branch__id=clientId)
        for raw in ordersQS:
            resp['data'].append(OrderSerializers(raw).data)

    except Exception as e:
        resp['code'] = None
        resp['msg'] = _('Can`t retrieve client orders')

    return Response(resp)
