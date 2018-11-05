'''
Django settings for AWS deployment
'''
# Need to set ENV_TYPE as environment variable in AWS console, e.g. ENV_TYPE='development'

import os
os.environ.setdefault('ENV_TYPE', 'test')
# os.environ.setdefault('ENV_TYPE', 'celerytest')
from .base import *
import secure


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True

# SECURE_SSL_REDIRECT = True

#### AMAZON S3 STATICFILES STORAGE ####
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = secure.AWS_STORAGE_BUCKET_NAME
AWS_S3_ACCESS_KEY_ID = secure.AWS_S3_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = secure.AWS_SECRET_ACCESS_KEY

# EMAIL settings
EMAIL_HOST = secure.EMAIL_HOST
EMAIL_PORT = secure.EMAIL_PORT
EMAIL_USE_TLS = secure.EMAIL_USE_TLS
EMAIL_HOST_USER = secure.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = secure.EMAIL_HOST_PASSWORD

ADMINS = secure.ADMINS
MANAGERS = secure.MANAGERS
SERVER_EMAIL = 'sam@sam'

# Get environment-specific database settings from secure.py
DATABASES = {
	'default': secure.AWS_DATABASE[os.environ['ENV_TYPE']]
}

#celery
CELERY_BROKER_URL = secure.AWS_CELERY_BROKER_URL
CELERY_BROKER_TRANSPORT_OPTIONS = {"region": "ap-southeast-1",
								   "polling_interval": 2,
								   'queue_name_prefix': 'celery-',
								   'visibility_timeout': 3600	
								  }

