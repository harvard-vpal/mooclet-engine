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

class VariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variable
        # fields = ('id','name','display_name','description')

class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = ('id','variable','user','mooclet','version','policy','value','text','timestamp')
        