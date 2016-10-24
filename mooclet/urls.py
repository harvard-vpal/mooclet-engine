from django.conf.urls import include, url
from rest_framework import routers
from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'mooclets', views.MoocletViewSet)
router.register(r'versions', views.VersionViewSet)
router.register(r'variables', views.VariableViewSet)
router.register(r'values', views.ValueViewSet)

urlpatterns = []
urlpatterns += router.urls