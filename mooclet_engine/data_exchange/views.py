# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import *
from .serializers import *
import requests
from rest_framework import viewsets
#import data_settings.py
import StringIO
import base64
import pandas as pd

import zipfile
try: import simplejson as json
except ImportError: import json

from django.core.files import File

from mooclet_engine.settings.secure import QUALTRICS_API_TOKEN, QUALTRICS_DATA_CENTER, QUALTRICS_DEFAULT_FILE_FORMAT, ONTASK_API_USER, ONTASK_API_PW


# Create your views here.


class BaseDataIntake():
	"""
	Base class for getting data from somewhere else. needs a url,
	possibly an encoding, and some settings (e.g. is this qualtrics, etc)
	"""

class BaseDataOutput():
	"""
	Base class for outputting data to somewhere else.
	Needs location to send data to, format
	"""


class QualtricsSurveyViewSet(viewsets.ModelViewSet):
    queryset = QualtricsSurvey.objects.all()
    #lookup_field = 'name'
    #multiple_lookup_fields = ('name', 'id')
    serializer_class = QualtricsSurveySerializer
    #filter_fields = ('mooclet', 'mooclet__name',)
    #search_fields = ('name', 'mooclet__name',)

class OnTaskWorkflowViewSet(viewsets.ModelViewSet):
    queryset = OnTaskWorkflow.objects.all()
    #lookup_field = 'name'
    #multiple_lookup_fields = ('name', 'id')
    serializer_class = OnTaskWorkflowSerializer
    #filter_fields = ('mooclet', 'mooclet__name',)
    #search_fields = ('name', 'mooclet__name',)

class QualtricsOnTaskDataExchangeViewSet(viewsets.ModelViewSet):
    queryset = QualtricsOnTaskDataExchange.objects.all()
    #lookup_field = 'name'
    #multiple_lookup_fields = ('name', 'id')
    serializer_class = QualtricsOnTaskDataExchangeSerializer
    #filter_fields = ('mooclet', 'mooclet__name',)
    #search_fields = ('name', 'mooclet__name',)


