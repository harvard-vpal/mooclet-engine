from rest_framework import serializers
from .models import Mooclet, Version, Learner, Variable, Value, Policy, PolicyParameters

class MoocletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mooclet
        fields = ('id', 'environment','mooclet_id', 'name', 'policy',)

class VersionSerializer(serializers.ModelSerializer):
    # environment = serializers.ReadOnlyField()
    #mooclet = MoocletSerializer()

    class Meta:
        model = Version
        # exclude = ('id',)
        fields = ('id', 'name','text','version_id','mooclet',)

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('id', 'environment','name')

class VariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variable
        fields = ('id', 'environment','variable_id','name',)

class ValueSerializer(serializers.ModelSerializer):
    # variable_name = serializers.RelatedField(source='Variable')
    variable = serializers.SlugRelatedField(slug_field='name', queryset=Variable.objects.all())
    learner = serializers.SlugRelatedField(slug_field='name', queryset=Learner.objects.all(), allow_null=True, required=False)
    #mooclet_name = serializers.SlugRelatedField(slug_field='name', queryset=Mooclet.objects.all(), allow_null=True)
    #version_name = serializers.SlugRelatedField(slug_field='name', queryset=Version.objects.all(), allow_null=True)
    class Meta:
        model = Value
        fields = ('id', 'variable','learner','mooclet','version','policy','value','text','timestamp',)

# class EnvironmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Environment
#         fields = ('name',)

class LearnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Learner
        fields = ('id', 'name', 'environment', 'learner_id')

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User

class PolicyParametersSerializer(serializers.ModelSerializer):
    parameters = serializers.JSONField()

    class Meta:
        model = PolicyParameters
        fields = ('id', 'mooclet', 'policy', 'parameters')