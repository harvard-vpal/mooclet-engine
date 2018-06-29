from rest_framework import serializers
from .models import QualtricsSurvey, OnTaskWorkflow, QualtricsOnTaskDataExchange



class QualtricsSurveySerializer(serializers.ModelSerializer):
	 class Meta:
	 	model = QualtricsSurvey
	 	fields = ('id', 'survey_id','url',)

class OnTaskWorkflowSerializer(serializers.ModelSerializer):
	 class Meta:
	 	model = OnTaskWorkflow
	 	fields = ('id', 'survey_id','url',)


class QualtricsOnTaskDataExchangeSerializer(serializers.ModelSerializer):
	 class Meta:
	 	model = QualtricsOnTaskDataExchange
	 	fields = ('id', 'data_input','data_output', 'shared_variables',)