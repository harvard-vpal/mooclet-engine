import requests
from django.conf import settings


def create_mooclet():
    r = requests.get("{}/{}".format(settings.MOOCLET_URL_BASE,'create_mooclet'))
    return r.json()

def create_version():
	pass

def create_variable():
	pass

def create_value():
	pass