import os
# set default environment variable before importing base settings
# os.environ.setdefault('ENV_TYPE', 'local')

from .base import *
import secure

DEBUG = True

ALLOWED_HOSTS = []

# INSTALLED_APPS += ('debug_toolbar', 'sslserver')

# MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': secure.LOCAL_DATABASE['dev'],
}

# For Django Debug Toolbar:
INTERNAL_IPS = ('127.0.0.1', '10.0.2.2',)

# DEBUG_TOOLBAR_CONFIG = {
#    'INTERCEPT_REDIRECTS': False,
# }


# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATIC_URL = '/static/'
# STATIC_ROOT = normpath(join(SITE_ROOT, 'http_static'))

DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000


#CELERY
CELERY_BROKER_URL = secure.LOCAL_CELERY_BROKER_URL