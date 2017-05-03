from rest_framework import serializers
from .models import Mooclet, Version, Learner, Variable, Value, Policy

class MoocletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mooclet
        fields = ('environment','mooclet_id', 'name', 'policy')

class VersionSerializer(serializers.ModelSerializer):
    # environment = serializers.ReadOnlyField()
    mooclet = MoocletSerializer()

    class Meta:
        model = Version
        # exclude = ('id',)
        fields = ('name','text','version_id','mooclet')

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('environment','name')

class VariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variable
        fields = ('environment','variable_id','name')

class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = ('variable','user','mooclet','version','policy','value','text','timestamp')

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User