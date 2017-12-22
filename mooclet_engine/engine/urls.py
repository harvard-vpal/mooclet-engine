from django.conf.urls import include, url
from rest_framework import routers
from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'mooclet', views.MoocletViewSet)
router.register(r'version', views.VersionViewSet)
router.register(r'variable', views.VariableViewSet)
router.register(r'value', views.ValueViewSet)
#router.register(r'valuepandas', views.PandasValueViewSet)
router.register(r'policy', views.PolicyViewSet)
router.register(r'learner', views.LearnerViewSet)
# router.register(r'user', views.UserViewSet)

urlpatterns = [
	url(r'^api/v1/', include(router.urls, namespace='api')),
	url(r'^data', views.PandasValueViewSet.as_view()),
	url(r'^learner-data', views.PandasLearnerValueViewSet.as_view())
]
