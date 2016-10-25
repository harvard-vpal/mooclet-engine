from django.shortcuts import render

from rest_framework import viewsets
from .serializers import *


class TextMoocletViewSet(viewsets.ModelViewSet):
    queryset = TextMooclet.objects.all()
    serializer_class = MoocletSerializer

    @detail_route()
    def get_version(self, request, pk=None):
    	params = request.GET
    	self.get_version(params)

class TextVersionViewSet(viewsets.ModelViewSet):
    queryset = TextVersion.objects.all()
    serializer_class = VersionSerializer
