'''
THIS FILE IS AN EXAMPLE ONLY!
NONE OF THE SETTINGS IN THIS FILE WILL WORK OUT OF THE BOX
RENAME THIS FILE TO secure.py 

Note - the .gitignore file is setup to exclude secure.py
from git. secure.py should never be put under version control.

'''

import os

os.environ.setdefault('ENV_TYPE', 'test')

# django secret key
SECRET_KEY = "",

MOOCLET_URL_BASE = {
    'local': 'http://localhost:8000/moocletengine/api',
    'test': 'https:///example.com/moocletengine/api',
}

AWS_DATABASE = {
    'test': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dbname',
        'USER': 'dbuser',
        'PASSWORD': 'dbpass',
        'HOST': 'xxx.us-east-1.rds.amazonaws.com',
        'PORT': 5432,
    }
}

ALLOWED_HOSTS = {
    'test': ['example.com'],
    'local': [],
}

# credentials for app-mooclet-engine IAM user
AWS_S3_ACCESS_KEY_ID = 'xxx'
AWS_SECRET_ACCESS_KEY = 'xxx'
AWS_STORAGE_BUCKET_NAME = 'my-bucket-name'
