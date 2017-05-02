from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

def home(request):
	return HttpResponse('Mooclet engine project')

