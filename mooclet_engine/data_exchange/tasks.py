from celery import Celery
from celery import shared_task
import requests
import pandas as pd
from django.utils import timezone
import zipfile
import os
import StringIO
import base64
import hashlib
try: import simplejson as json
except ImportError: import json
from mooclet_engine.settings.secure import QUALTRICS_API_TOKEN, QUALTRICS_DATA_CENTER, QUALTRICS_DEFAULT_FILE_FORMAT, ONTASK_API_USER, ONTASK_API_PW
from models import *
from engine.models import *
from utils import OnTask


@shared_task
def get_qualtrics_data(self, **kwargs):
	api_token = QUALTRICS_API_TOKEN
	data_center = QUALTRICS_DATA_CENTER
	file_format = QUALTRICS_DEFAULT_FILE_FORMAT

	#pass pk of qualtrics survey  database as "qualtrics_survey"
	survey = QualtricsSurvey.objects.get(pk=kwargs["qualtrics_survey"])
	survey_id = survey.survey_id

	last_export_date = survey.last_export_date

	last_respondent = survey.last_survey_respondent

	# Setting static parameters
	requestCheckProgress = 0
	progressStatus = "in progress"
	baseUrl = "https://{0}.qualtrics.com/API/v3/responseexports/".format(data_center)
	headers = {
    	"content-type": "application/json",
    	"x-api-token": api_token,
    	}

	# Step 1: Creating Data Export
	downloadRequestUrl = baseUrl
	downloadRequestPayload = {"format": file_format,
							  "surveyId": survey_id}
	if last_export_date:
		last_export_date = last_export_date.isoformat()
		print last_export_date
		downloadRequestPayload["startDate"] = last_export_date

	if last_respondent:
		downloadRequestPayload["lastResponseId"] = last_respondent

	downloadRequestPayload = json.dumps(downloadRequestPayload)
	print downloadRequestPayload
	#req='{"format":"' + file_format + '","surveyId":"' + survey_id + '","lastResponseId":"' + last_respondent + '"}'
	downloadRequestResponse = requests.request("POST", downloadRequestUrl, data=downloadRequestPayload, headers=headers)
	print downloadRequestResponse.json()
	progressId = downloadRequestResponse.json()["result"]["id"]
	print downloadRequestResponse.text

	# Step 2: Checking on Data Export Progress and waiting until export is ready
	while requestCheckProgress < 100 and progressStatus is not "complete":
  		requestCheckUrl = baseUrl + progressId
  		requestCheckResponse = requests.request("GET", requestCheckUrl, headers=headers)
  		requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]
  		print "Download is " + str(requestCheckProgress) + " complete"


	# Step 3: Downloading file
	requestDownloadUrl = baseUrl + progressId + '/file'
	requestDownload = requests.request("GET", requestDownloadUrl, headers=headers, stream=True)

	# Step 4: Unziping file
	with open("RequestFile.zip", "wb") as f:
		for chunk in requestDownload.iter_content(chunk_size=1024):
			f.write(chunk)

	zipped = zipfile.ZipFile("RequestFile.zip")
	zipinfo = zipped.infolist()
	unzipped = zipped.extract(zipinfo[0])
	print unzipped

	with open(unzipped, 'r') as f:
		survey_data = json.load(f)

	print survey_data
	responses = survey_data["responses"]

	for response in responses:
		if "user_id" in response:
			learner, created = Learner.objects.get_or_create(name=response["user_id"])
		else:
			learner, created = Learner.objects.get_or_create(name=response["ResponseID"])
		for item in response:
			if response[item]:
				variable, created = Variable.objects.get_or_create(name=item)
				val_num = None
				try:
					val_num = float(response[item])
				except:
					pass
				value = Value.objects.create(variable=variable,
											 learner=learner,
											 text=response[item],
											 value=val_num
											)
				value.save()





	os.remove("RequestFile.zip")
	os.remove(unzipped)


	last_export_date = timezone.now()
	survey.last_export_date = last_export_date
	survey.save()


@shared_task
def update_workflow_data(self, **kwargs):
	workflow = OnTaskWorkflow.objects.get(pk=kwargs["ontask_workflow"])
	workflow_id = workflow.workflow_id

	data_exchanges = workflow.qualtricsontaskdataexchange_set.all()

	workflow_object = OnTask(workflow_id)

	workflow_object.lock()
	result_df = workflow_object.read()
	

	print result_df
	print list(result_df)

	#assume we have a field "email" storing emails
	result_df['hashed_id'] = result_df['email'].apply(lambda x: hash_and_save(x))#['email']
	#just recalculate the hash for everyone
	# if 'hashed_id' not in result_df.columns:
	# 	result_df['hashed_id'] = result_df.get['email'].apply(lambda x: hash_and_save(x))#['email']

	# else:
	# 	result_df['hashed_id'] = result_df.apply(lambda x: hash_and_save(x['email'], x['hashed_id']), axis=0)

	print result_df

	if data_exchanges:
		#mooclets = Mooclets.objects.all()
		for data_exchange in data_exchanges:
	 		mooclets = data_exchange.mooclets.all()
	 		for mooclet in mooclets:
	 			result_df[mooclet.name + "_version"], result_df[mooclet.name + "_text"] = result_df.apply(lambda x: run_version_if_none(x, mooclet), axis=1)



	updated_workflow = workflow_object.update(result_df)
	print updated_workflow
	print updated_workflow.content

	workflow_object.unlock()


def run_version_if_none(row, mooclet):
	learner, created = Learner.objects.get_or_create(name=row['hashed_id'])
	print row
	if mooclet.name + '_version' not in row and mooclet.name + '_text' not in row:
		print "no mooclet row"
		version = mooclet.run(context={"learner":learner})
		return version.name, version.text

	elif not row[mooclet.name + "_version"] and not row[mooclet.name + "_text"]:
		print "row but no values"
		version = mooclet.run(context={"learner":learner})
		return version.name, version.text

	else:
		print "row and value"
		return row[mooclet.name + "_version"], row[mooclet.name + "_text"]


	






def hash_and_save(email, hashed=None):

	user_hash = hashlib.sha512(email).hexdigest()
	learner,created = Learner.objects.get_or_create(name=user_hash)

	return user_hash





