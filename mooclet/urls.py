from django.conf.urls import include, url
from rest_framework import routers
from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'mooclets', views.MoocletViewSet)
router.register(r'versions', views.VersionViewSet)

urlpatterns = []
urlpatterns += router.urls