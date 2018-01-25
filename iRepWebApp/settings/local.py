from base import *
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'..', "static"),
)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'irep',
        'HOST': 'localhost',
        'PORT': '5432',
        'USER': 'postgres',
        'PASSWORD': 'postgres'
    }
}



# MEDIA_URL = os.path.join(BASE_DIR, '..')+'/'

#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'db',
#     }
# }
#
#
# INSTALLED_APPS = [
#     'grappelli',
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'django.contrib.sites',
#     'django.contrib.humanize',
#     'allauth',
#     'allauth.account',
#     'allauth.socialaccount',
#     'iRep',
#     'notifications',
#     'cities_light',
#     'endless_pagination',
#     'rosetta',
#     # 'import_export',
#     'crispy_forms',
#     'widget_tweaks',
#     'rest_framework',
#
# ]