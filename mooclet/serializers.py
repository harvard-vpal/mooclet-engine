from rest_framework import serializers
from .models import *

class MoocletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mooclet
        fields = ('id', 'name', 'policy')

class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ('id','mooclet','name')

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('id','name')