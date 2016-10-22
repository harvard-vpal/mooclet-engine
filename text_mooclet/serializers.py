from rest_framework import serializers
from .models import *

class MoocletSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextMooclet

    @detail_route()
    def get_version(self, request, pk=None):
    	params = request.GET
    	self.get_version(params)
        

class VersionSerializer(serializers.ModelSerializer):
    class Meta:
    	model = TextVersion
