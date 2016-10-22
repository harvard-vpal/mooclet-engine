from django.shortcuts import render

from rest_framework import viewsets
from .serializers import *


class TextMoocletViewSet(viewsets.ModelViewSet):
    queryset = TextMooclet.objects.all()
    serializer_class = MoocletSerializer

class TextVersionViewSet(viewsets.ModelViewSet):
    queryset = TextVersion.objects.all()
    serializer_class = VersionSerializer
