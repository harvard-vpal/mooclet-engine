from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
	
    url(r'^$', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^moocletengine/', include('mooclet_engine.urls', namespace="mooclet_engine")),


]
