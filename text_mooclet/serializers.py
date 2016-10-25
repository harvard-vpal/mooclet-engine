from rest_framework import serializers
from .models import *

class MoocletSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextMooclet      

class VersionSerializer(serializers.ModelSerializer):
    class Meta:
    	model = TextVersion
