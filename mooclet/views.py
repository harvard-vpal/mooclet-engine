from rest_framework import viewsets
from .serializers import *


# rest framework viewsets
class MoocletViewSet(viewsets.ModelViewSet):
    queryset = Mooclet.objects.all()
    serializer_class = MoocletSerializer

class VersionViewSet(viewsets.ModelViewSet):
	queryset = Version.objects.all()
	serializer_class = VersionSerializer

