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







class QualtricsGetData():
    #api_token = data_settings.QUALTRICS_API_TOKEN

    #base_url = data_settings.QUALTRICS_BASE_URL
    fileFormat = 'json'



    # def get_data(survey):
    #     survey_id = survey.survey_id

    #     headers = {"X-API-TOKEN": api_token, "content-type": "application/json"}

    #     fileFormat = 'json'

    #     # Step 1: Creating Data Export
    #     downloadRequestUrl = base_url
    #     downloadRequestPayload = '{"format":"' + fileFormat + '","surveyId":"' + survey_id + '"}'
    #     downloadRequestResponse = requests.request("POST", downloadRequestUrl, data=downloadRequestPayload, headers=headers)
    #     progressId = downloadRequestResponse.json()["result"]["id"]
    #     print downloadRequestResponse.text

    #     # Step 2: Checking on Data Export Progress and waiting until export is ready
    #     while requestCheckProgress < 100 and progressStatus is not "complete":
    #         requestCheckUrl = base_url + progressId
    #         requestCheckResponse = requests.request("GET", requestCheckUrl, headers=headers)
    #         requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]
    #         print "Download is " + str(requestCheckProgress) + " complete"


    #     # Step 3: Downloading file
    #     requestDownloadUrl = baseUrl + progressId + '/file'
    #     requestDownload = requests.request("GET", requestDownloadUrl, headers=headers, stream=True)

    #     # Step 4: Unziping file
    #     with open("RequestFile.zip", "wb") as f:
    #         for chunk in requestDownload.iter_content(chunk_size=1024):
    #             f.write(chunk)
    #     zipfile.ZipFile("RequestFile.zip").extractall("MyQualtricsDownload")


    #     pass


class OnTask():
    base_url = "https://ontasklearning.com/"
    api_user = ONTASK_API_USER
    api_pw = ONTASK_API_PW
    connect_timeout = 5.0
    read_timeout = 30.0

    

    def __init__(self, workflow_id):
        self.workflow_id = workflow_id
        self.session = requests.Session()
        self.session.auth = (self.api_user, self.api_pw)

    def lock(self):
        url = self.base_url + "workflow/" + str(self.workflow_id) + "/lock"
        response = self.session.post(url, timeout=(self.connect_timeout, self.read_timeout))
        return response

    def unlock(self):
        url = self.base_url + "workflow/" + str(self.workflow_id) + "/lock"
        response = self.session.delete(url)
        return response

    def read(self):
        url = self.base_url + "table/" + str(self.workflow_id) + "/pops/"
        response = self.session.get(url, timeout=(self.connect_timeout, self.read_timeout))
        if response.status_code != 200:
            print response
            return response
        else:
            workflow_data = response.json()
            workflow_data = workflow_data["data_frame"]

            output = StringIO.StringIO()
            output.write(base64.b64decode(workflow_data))
            result_df = pd.read_pickle(output)
            print result_df
            return result_df


    def update(self, data_frame):
        url = self.base_url + "table/" + str(self.workflow_id) + "/pops/"
        out_file = StringIO.StringIO()
        pd.to_pickle(data_frame, out_file)
        result = base64.b64encode(out_file.getvalue())

        response = self.session.put(url, data={"data_frame":result}, timeout=(self.connect_timeout, self.read_timeout))
        return response