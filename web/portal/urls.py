import sys
sys.path.append('../')


from django.conf.urls import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers
from rest_framework import permissions
from django.urls import path

from web.portal.index import *
from web.portal import api

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

router = routers.DefaultRouter()

schema_view = get_schema_view(
   openapi.Info(
      title="Willz API",
      default_version='v1',
      description="This is the description of Willz API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router.register(r'api/clients', api.ClientApi)
router.register(r'api/individuals', api.IndividualsApi)
router.register(r'api/tasks/client_task', api.ClientTaskApi)
router.register(r'api/tasks', api.TasksModelApi)
router.register(r'api/willz', api.RawClientData)

urlpatterns = [

    url(r'^$', index),
    url(r'^', include(router.urls)),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/willz/', api.WillzCreateClient.as_view()),
 ]
