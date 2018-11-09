from django.conf.urls import include, url
from rest_framework import routers
from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'qualtricssurvey', views.QualtricsSurvey)
router.register(r'ontaskworkflow', views.OnTaskWorkflow)
router.register(r'qualtricsontaskdataexchange', views.QualtricsOnTaskDataExchange)


urlpatterns = [
	url(r'^dataexchange/', include(router.urls, namespace='dataexchange')),

]