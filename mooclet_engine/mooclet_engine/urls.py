from django.conf.urls import url, include
from django.contrib import admin
from . import views
from rest_framework.documentation import include_docs_urls

urlpatterns = [
	url(r'^engine/', include('engine.urls', namespace="engine")),
	url(r'^docs/', include_docs_urls(title='MOOClet API Documentation', public=False)),
	url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='home'),
]
