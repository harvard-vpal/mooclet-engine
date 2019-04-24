from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery import shared_task
import requests
import numpy as np
import pandas as pd
from django.utils import timezone
import tempfile
import zipfile
import os
import StringIO
import base64
import hashlib
import datetime
try: import simplejson as json
except ImportError: import json
from mooclet_engine.settings.secure import QUALTRICS_API_TOKEN, QUALTRICS_DATA_CENTER, QUALTRICS_DEFAULT_FILE_FORMAT, ONTASK_API_USER, ONTASK_API_PW
from .models import *
from engine.models import *
from .utils import OnTask
from engine.utils.utils import *
from engine.policies import *

#write the new batch updating task

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
	temp_zip, temp_zip_path = tempfile.mkstemp()
	with open(temp_zip_path, "w") as f:
		for chunk in requestDownload.iter_content(chunk_size=1024):
			f.write(chunk)

	zipped = zipfile.ZipFile(temp_zip_path)
	zipinfo = zipped.infolist()
	#unzipped = StringIO.StringIO()
	with zipped.open(zipinfo[0]) as f:
	#with open(unzipped, 'r') as f:
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





	os.remove(temp_zip_path)
	#os.remove(unzipped)


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
	 			print "mooclet: " + mooclet.name
	 			if mooclet.name + "_version" not in result_df:
	 				result_df[mooclet.name + "_version"] = ""
	 			if mooclet.name + "_text" not in result_df:
	 				result_df[mooclet.name + "_text"] = ""
	 			result_df[[mooclet.name + "_version", mooclet.name + "_text"]] = result_df.apply(lambda x: run_version_if_none(x, mooclet), axis=1)
	 	print result_df


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
		version_info = {mooclet.name + "_version": version.name, mooclet.name + "_text": version.text}
		
		print version_info
		version_info = pd.Series(version_info)
		return version_info

	elif not row[mooclet.name + "_version"] and not row[mooclet.name + "_text"]:
		print "row but no values"
		version = mooclet.run(context={"learner":learner})
		version_info = {mooclet.name + "_version": version.name, mooclet.name + "_text": version.text}
		print version_info
		version_info = pd.Series(version_info)
		return version_info

	else:
		print "row and value"
		return row[mooclet.name + "_version"], row[mooclet.name + "_text"]


	






def hash_and_save(email, hashed=None):

	user_hash = hashlib.sha512(email).hexdigest()
	learner,created = Learner.objects.get_or_create(name=user_hash)

	return user_hash


@shared_task
def update_model(self, **kwargs):
	mooclet = Mooclet.objects.get(pk=kwargs["mooclet"])
	policy = Policy.objects.get(pk=kwargs["policy"])
	params = PolicyParameters.objects.get(mooclet=mooclet, policy=policy)
	parameters = params.parameters

	regression_formula = parameters['regression_formula']
	# Get current priors parameters (normal-inverse-gamma)
	mean = parameters['coef_mean']
	cov = parameters['coef_cov']
	variance_a = parameters['variance_a']
	variance_b = parameters['variance_b']
	latest_update = params.latest_update
	values = values_to_df(mooclet, params, latest_update)
	
	if not values.empty:
		print("has new values!")
		new_history = PolicyParametersHistory.create_from_params(params)
		new_update_time = datetime.datetime.now()
		params.latest_update = new_update_time
		params.save()
		rewards = values[parameters['outcome_variable']]
		values = values.drop(["user_id", parameters['outcome_variable']], axis=1)

		design_matrix = create_design_matrix(values, regression_formula)
		numpy_design_matrix = design_matrix.values
		numpy_rewards = rewards.values
		posterior_vals = posteriors(numpy_rewards, numpy_design_matrix, mean, cov, variance_a, variance_b)
		print("posteriors: " + str(posterior_vals))
		params.parameters['coef_mean'] = posterior_vals["coef_mean"].tolist()
		params.parameters['coef_cov'] = posterior_vals["coef_cov"].tolist()
		params.parameters['variance_a'] = posterior_vals["variance_a"]
		params.parameters['variance_b'] = posterior_vals["variance_b"]
		params.save()







