from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer, UniqueFieldsMixin
from .models import Mooclet, Version, Learner, Variable, Value, Policy, PolicyParameters, PolicyParametersHistory

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
        version_json = serializers.JSONField(source='version_json')
        fields = ('id', 'name','text','version_id','mooclet', 'version_json')

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ('id', 'environment','name')

class VariableSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Variable
        fields = ('id', 'environment','variable_id','name',)

class ValueSerializer(WritableNestedModelSerializer):
    # variable_name = serializers.RelatedField(source='Variable')
    #variable = VariableSerializer(allow_null=False)
    variable = serializers.SlugRelatedField(slug_field='name', queryset=Variable.objects.all())
    learner = serializers.SlugRelatedField(slug_field='name', queryset=Learner.objects.all(), allow_null=True, required=False)
    #mooclet_name = serializers.SlugRelatedField(slug_field='name', queryset=Mooclet.objects.all(), allow_null=True)
    #version_name = serializers.SlugRelatedField(slug_field='name', queryset=Version.objects.all(), allow_null=True)
    class Meta:
        model = Value
        fields = ('id', 'variable','learner','mooclet','version','policy','value','text','timestamp',)

    # def validate_variable(self ,variable):
    #     print "validating"
    #     return variable

    # def create(self, validated_data):
    #     print "starting create"
    #     var_name = validated_data.pop('variable')
    #     var = Variable.objects.get_or_create(name=var_name)
    #     var.save()
    #     val = Value.objects.create(variable=var, **validated_data)
    #     return val
        # try:
        #     var = Variable.objects.get(name=validated_data.name)
        #     print "var exists"
        #     return Value(**validated_data)
        # except:
        #     var = Variable.objects.create(name=validated_data.name)
        #     var.save()
        #     print "saved new var"
        #     return Value(**validated_data)


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
    class Meta:
        model = PolicyParameters
        parameters = serializers.JSONField(source='parameters')
        fields = ('id', 'mooclet', 'policy', 'parameters')

class PolicyParametersHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyParametersHistory
        parameters = serializers.JSONField(source='parameters')
        fields = ('id', 'mooclet', 'policy', 'parameters', 'creation_time')
