from base import *
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'irep',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',  # '127.0.0.1'
        'PORT': '5432',  # '5556'
    }
}
