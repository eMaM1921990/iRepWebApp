from django.views.decorators.cache import never_cache
from django.views.decorators.gzip import gzip_page
from rest_framework.decorators import api_view
from rest_framework.response import Response

from iRep.Serializers import SalesForceSerializer, ProductSerializer, ProductGroupSerializer
from iRep.models import SalesForce, ProductGroup
from django.utils.translation import ugettext_lazy as _

@gzip_page
@never_cache
@api_view(['POST'])
def SalesForceLogin(request):
    resp = {}
    resp['code'] = None
    # validations
    if 'user_pin' not in request.POST:
        resp['code'] = None
        resp['msg'] = _('Missing user pin.')
        return Response(resp)

    if 'password' not in request.POST:
        resp['code'] = None
        resp['msg'] = _('Missing password')
        return Response(resp)

    if 'corp_id' not in request.POST:
        resp['code'] = None
        resp['msg'] = _('Missing corpId')
        return Response(resp)

    try:
        profile = SalesForce.objects.get(user_pin=request.POST['user_pin'],
                                         password_pin=request.POST['password'],
                                         corp_id=request.POST['corp_id'])

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
