"""
WSGI config for iRepWebApp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iRepWebApp.settings")
#
# application = get_wsgi_application()



import os
import sys

sys.path.append('/opt/bitnami/apps/django/django_projects/iRepWebApp')
os.environ['PYTHON_EGG_CACHE']="/opt/bitnami/apps/django/django_projects/iRepWebApp/egg_cache"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iRepWebApp.settings.")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
