from django.core.exceptions import PermissionDenied

from iRep.models import Corporate

__author__ = 'eMaM'


def user_is_same_company(function):
    def wrap(request, *args, **kwargs):
        corporate = Corporate.objects.get(slug=kwargs['slug'])
        if corporate.created_by == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap
