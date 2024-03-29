__author__ = 'eMaM'

from django.shortcuts import render_to_response
from django.template import RequestContext


def error_forbidden(request):
    response = render_to_response('403.html', context_instance=RequestContext(request))
    response.status_code = 404
    return response
