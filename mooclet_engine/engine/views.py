from rest_framework import viewsets
from rest_pandas import PandasView
from .models import *
from .serializers import *
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import pandas as pd
import json

# rest framework viewsets

class MoocletViewSet(viewsets.ModelViewSet):
    """
    MOOClets are the building blocks of experiments/RCTs via web service.

    retrieve:
        Return the given MOOClet.

    list:
        Return a list of all the existing MOOClets.

    create:
        Create a new MOOClet instance.
    """

    queryset = Mooclet.objects.all()
    serializer_class = MoocletSerializer
    #lookup_field = 'name'
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
        elif request.GET.get('learner', None):
            learner, created = Learner.objects.get_or_create(name=request.GET.get('learner', None))
        context['learner'] = learner
        version = self.get_object().run(context=context)
        #print version
        Version, created = Variable.objects.get_or_create(name='version')
        #TODO: clean this up
        if type(version) is dict:
            version_id = version['id']
            version_name = version['name']
            serialized_version = version
        else:
            version_id = version.id
            version_name = version.name
            serialized_version = VersionSerializer(version).data

        version_shown = Value( 
                            learner=learner,
                            variable=Version,
                            mooclet=self.get_object(),
                            version_id=version_id,
                            value=version_id,
                            text=version_name
                            )
        version_shown.save()
        return Response(serialized_version)

class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    #lookup_field = 'name'
    multiple_lookup_fields = ('name', 'id')
    serializer_class = VersionSerializer
    filter_fields = ('mooclet', 'mooclet__name',)
    search_fields = ('name', 'mooclet__name',)

    # def get_object(self):
    #     queryset = self.get_queryset()
    #     filter = {}
    #     for field in self.multiple_lookup_fields:
    #         try:
    #             filter[field] = self.kwargs[field]
    #         except:
    #             pass

    #     obj = get_object_or_404(queryset, **filter)
    #     self.check_object_permissions(self.request, obj)
    #     return obj

class VersionNameViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    #lookup_field = 'name'
    multiple_lookup_fields = ('name', 'id')
    serializer_class = VersionSerializer
    filter_fields = ('mooclet', 'mooclet__name',)
    search_fields = ('name', 'mooclet__name',)

class VariableViewSet(viewsets.ModelViewSet):
    queryset = Variable.objects.all()
    #lookup_field = 'name'
    serializer_class = VariableSerializer
    search_fields = ('name',)

class ValueViewSet(viewsets.ModelViewSet):
    queryset = Value.objects.all()
    serializer_class = ValueSerializer
    filter_fields = ('learner', 'variable', 'learner__name', 'variable__name', 'mooclet', 'mooclet__name', 'version', 'version__name',)
    search_fields = ('learner__name', 'variable__name',)
    ordering_fields = ('timestamp','learner', 'variable', 'learner__name', 'variable__name', 'mooclet', 'mooclet__name', 'version', 'version__name',)

    @list_route(methods=['POST'])
    def create_many(self, request, pk=None):
        queryset = Value.objects.all()
        serializer = ValueSerializer(many=True, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response({'error':'invalid'}, status=500)

    @list_route(methods=['POST'])
    def create_many_fromobj(self, request, pk=None):
        queryset = Value.objects.all()
        print("Data:")
        print(request.data)

        vals = request.data[request.data.keys()[0]]
        try:
            vals = json.loads(vals)
        except:
            pass
        serializer = ValueSerializer(many=True, data=vals)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response({'error':'invalid'}, status=500)

class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    #lookup_field = 'name'
    search_fields = ('name',)

class LearnerViewSet(viewsets.ModelViewSet):
    queryset = Learner.objects.all()
    #lookup_field = 'name'
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
        data = dataframe
        data1= data.pivot_table(index='id', columns='variable')['value']
        data = pd.concat([data,data1],axis=1).set_index('learner')
        del data['variable'],data['value']#,data['index']
        list_ = data.columns
        data_transformed = data.groupby(level=0).apply(lambda x: x.values.ravel()).apply(pd.Series)

        for f in data_transformed.columns:
            data_transformed=data_transformed.rename(columns={f:list_[int(f)%len(list_)]+'_a'+str(int(f/len(list_))+1)})
            #dataframe.some_pivot_function(in_place=True)
        return data_transformed

# class EnvironmentViewSet(viewsets.ModelViewSet):
#     queryset = Environment.objects.all()
#     serializer_class = EnvironmentSerializer

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class PolicyParametersViewSet(viewsets.ModelViewSet):
    queryset = PolicyParameters.objects.all()
    serializer_class = PolicyParametersSerializer
    filter_fields = ('mooclet', 'policy')

class PolicyParametersHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PolicyParametersHistory.objects.all()
    serializer_class = PolicyParametersHistorySerializer
    filter_fields = ('mooclet', 'policy')