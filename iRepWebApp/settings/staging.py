from base import *
ALLOWED_HOSTS = ['160.153.237.158']

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


STATIC_ROOT = 'static/'




# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'irep_log.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'iRep': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}
