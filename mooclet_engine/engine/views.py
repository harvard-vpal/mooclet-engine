from rest_framework import viewsets
from rest_pandas import PandasView
from .models import *
from .serializers import *
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# rest framework viewsets

class MoocletViewSet(viewsets.ModelViewSet):
    queryset = Mooclet.objects.all()
    serializer_class = MoocletSerializer
    search_fields = ('name',)

    @detail_route()
    def test(self, request, pk=None):
        return Response({'test':'hi'})

    @detail_route()
    def run(self, request, pk=None):
        policy = request.GET.get('policy',None)
        context = {}
        learner = None
        if request.GET.get('user_id', None):
            learner, created = Learner.objects.get_or_create(name=request.GET.get('user_id', None))
            context['learner'] = learner
        version = self.get_object().run(context=context)
        Version, created = Variable.objects.get_or_create(name='version')
        version_shown = Value( 
                            learner=learner,
                            variable=Version,
                            mooclet=self.get_object(),
                            version=version,
                            value=version.id,
                            text=version.name
                            )
        version_shown.save()
        return Response(VersionSerializer(version).data)

class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    filter_fields = ('mooclet', 'mooclet__name',)
    search_fields = ('name', 'mooclet__name',)

class VariableViewSet(viewsets.ModelViewSet):
    queryset = Variable.objects.all()
    serializer_class = VariableSerializer
    search_fields = ('name',)

class ValueViewSet(viewsets.ModelViewSet):
    queryset = Value.objects.all()
    serializer_class = ValueSerializer
    filter_fields = ('learner', 'variable', 'learner__name', 'variable__name', 'mooclet', 'mooclet__name', 'version', 'version__name',)
    search_fields = ('learner__name', 'variable__name',)

    @list_route(methods=['POST'])
    def create_many(self, request, pk=None):
        queryset = Value.objects.all()
        serializer = ValueSerializer(many=True, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response({'error':'invalid'})

class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    search_fields = ('name',)

class LearnerViewSet(viewsets.ModelViewSet):
    queryset = Learner.objects.all()
    serializer_class = LearnerSerializer
    search_fields = ('name',)

class PandasValueViewSet(PandasView):
    queryset = Value.objects.all()
    serializer_class = ValueSerializer
    filter_fields = ('learner', 'variable', 'learner__name', 'variable__name', 'mooclet', 'mooclet__name', 'version', 'version__name',)
    search_fields = ('learner__name', 'variable__name',)


class PandasLearnerValueViewSet(PandasView):
    queryset = Value.objects.all()
    serializer_class = ValueSerializer
    filter_fields = ('learner', 'variable', 'learner__name', 'variable__name', 'mooclet', 'mooclet__name', 'version', 'version__name',)
    search_fields = ('learner__name', 'variable__name',)

    def transform_dataframe(self, dataframe):
        dataframe = dataframe.pivot_table(index='learner', columns='variable', values=['value', 'text'], aggfunc='first')
        #dataframe.some_pivot_function(in_place=True)
        return dataframe

# class EnvironmentViewSet(viewsets.ModelViewSet):
#     queryset = Environment.objects.all()
#     serializer_class = EnvironmentSerializer

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
