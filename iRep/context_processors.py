from django.conf import settings

__author__ = 'eMaM'


def google_map(request):
    mapKey = getattr(settings, 'GOOGLE_MAP_KEY', False)
    if mapKey:
        return {
            'GOOGLE_MAP_KEY': mapKey
        }
    return {}
