from base import *
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djangostack',
        'HOST': '/opt/bitnami/postgresql',
        'PORT': '5432',
        'USER': 'bitnami',
        'PASSWORD': '31f50ea6e1'
    }
}


STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
