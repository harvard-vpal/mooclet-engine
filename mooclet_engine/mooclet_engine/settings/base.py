"""
Django settings for mooclet_engine_project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import abspath, basename, dirname, join, normpath
from django.core.urlresolvers import reverse_lazy
from sys import path
import secure

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE DIR refers to the directory containing manage.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Absolute filesystem path to the Django project config directory:
# (this is the parent of the directory where this file resides,
# since this file is now inside a 'settings' pacakge directory)
DJANGO_PROJECT_CONFIG = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
# (this is one directory up from the project config directory)
SITE_ROOT = dirname(DJANGO_PROJECT_CONFIG)

# Site name:
SITE_NAME = basename(SITE_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(SITE_ROOT)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secure.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = secure.ALLOWED_HOSTS[os.environ['ENV_TYPE']]

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    ## external apps
    'storages',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
     ## internal apps
    'engine',
    'data_exchange',

    #celery
    'celery',
    'django_celery_results',
    'django_celery_beat',
    # 'ordered_model',
    # 'bootstrap3',
    # 'django_bootstrap_breadcrumbs',
    # 'crispy_forms',

   
    # 'text_mooclet',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS':[
        normpath(join(SITE_ROOT, 'templates')),
    ],
    'OPTIONS':{
        'context_processors': [
            # django auth
            'django.contrib.auth.context_processors.auth',

            # access the request inside django template
            'django.template.context_processors.request',
            # 'django.template.context_processors.debug',

            # enable django messages
            'django.contrib.messages.context_processors.messages',
        ],
        'loaders': [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ],
        'debug':True,
    },
},]

ROOT_URLCONF = 'mooclet_engine.urls'

WSGI_APPLICATION = 'mooclet_engine.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# Note - if you configure a database, you can store the database
# access credentials in the secure.py file. Just make sure that
# you do not remove secure.py from the .gitignore file. secure.py
# should never be uploaded to git. Secure.py.example is there to
# show you what secure.py should look like.



# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    normpath(join(SITE_ROOT, 'static')),
)

#### django-bootstrap ####
BOOTSTRAP3 = {
    'include_jquery':True,
}

#### DJANGO REST FRAMEWORK SETTINGS ####

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_AUTHENTICATION_CLASSES':(
        # for browsable api view usage
        'rest_framework.authentication.BasicAuthentication',
        #'rest_framework.authentication.SessionAuthentication',

        'rest_framework.authentication.TokenAuthentication',

    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
}

#### cors headers ####

# allow cross origin requests
CORS_ORIGIN_ALLOW_ALL = True


### versioning settings ###

DEFAULT_VERSION = 'v1'


### celery ###
CELERY_RESULT_BACKEND = 'django-db'
#CELERY_RESULT_BACKEND = 'django-cache'



CELERY_IMPORTS = ['engine', 'data_exchange.tasks']


#### custom application settings ####

# set envrionment-specific api url for mooclet engine, from secure.py
# MOOCLET_URL_BASE = secure.MOOCLET_URL_BASE[os.environ['ENV_TYPE']]

