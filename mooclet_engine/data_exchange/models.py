# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from engine.models import Variable, Mooclet

# Create your models here.



class AbstractDataExchange(models.Model):
	"""
	Input and output - should be FKs?
	"""
	data_input = models.CharField(max_length=2000) #url?
	data_output = models.CharField(max_length=2000) #url?

	class Meta:
		abstract = True

class QualtricsSurvey(models.Model):
	survey_id = models.CharField(max_length=200)
	url = models.URLField(max_length=2048, null=True, blank=True)
	last_survey_respondent = models.CharField(max_length=200, null=True, blank=True)
	last_export_date = models.DateTimeField(null=True, blank=True) #update timestamp on save

	def __unicode__(self):
		return self.survey_id

class OnTaskWorkflow(models.Model):
	workflow_id = models.IntegerField()
	url = models.URLField(max_length=2048, null=True, blank=True)

	def __unicode__(self):
		return str(self.workflow_id)

class QualtricsOnTaskDataExchange(AbstractDataExchange):
	data_input = models.ForeignKey('QualtricsSurvey')
	data_output = models.ForeignKey('OnTaskWorkflow')
	shared_variables = models.ManyToManyField(Variable, blank=True)
	mooclets = models.ManyToManyField(Mooclet, blank=True)