from rest_framework import viewsets
from .serializers import *
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# rest framework viewsets

class MoocletViewSet(viewsets.ModelViewSet):
    queryset = Mooclet.objects.all()
    serializer_class = MoocletSerializer

    @detail_route()
    def test(self, request, pk=None):
        return Response({'test':'hi'})

    @detail_route()
    def run(self, request, pk=None):
        policy = request.GET.get('policy',None)
        context = {}
        if request.GET.get('user_id'):
            context['learner'] = get_object_or_404(Learner, id=request.GET.get('user_id', None))
        version = self.get_object().run(context=context)
        return Response(VersionSerializer(version).data)

class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer

class VariableViewSet(viewsets.ModelViewSet):
    queryset = Variable.objects.all()
    serializer_class = VariableSerializer

class ValueViewSet(viewsets.ModelViewSet):
    queryset = Value.objects.all()
    serializer_class = ValueSerializer
    filter_fields = ('learner',)

class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer

class LearnerViewSet(viewsets.ModelViewSet):
    queryset = Learner.objects.all()
    serializer_class = LearnerSerializer

# class EnvironmentViewSet(viewsets.ModelViewSet):
#     queryset = Environment.objects.all()
#     serializer_class = EnvironmentSerializer

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
