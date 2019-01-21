import sys
sys.path.append('../')


from django.conf.urls import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers
from rest_framework import permissions
from django.urls import path

from web.portal import api
from .views import *
from .controllers.auth import *

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
# Работа с новой заявкой
router.register(r'api/willz', api.RawClientData)

# Работа с клиентскими данными
router.register(r'api/clients', api.ClientApi)
#router.register(r'api/generation', api.GetFullClientApi)
router.register(r'api/individuals', api.IndividualsApi)
router.register(r'api/passports', api.PassportsApi)
router.register(r'api/driver_licenses', api.DriverLicesesApi)
router.register(r'api/images', api.ImagesApi)


# Работа с тасками
router.register(r'api/tasks', api.TasksModelApi)
#router.register(r'api/tasks/client_task', api.ClientTaskApi)
#router.register(r'api/tasks/scoring_task', api.ClientTaskApi)
#router.register(r'api/tasks/source_task', api.ClientTaskApi)
#router.register(r'api/tasks/checks_task', api.ClientTaskApi)

# Работа с генерацией
router.register(r'api/generation', api.GenerationCreateApi)


urlpatterns = [
    url(r'^$', sign_in, name="signup"),
    url(r'^', include(router.urls)),

    url(r'^signup/$', sign_up, name='signup'),
    url(r'signin/$', sign_in, name="signin"),
    url(r'signout/$', sign_out, name="signout"),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/willz/', api.WillzCreateClient.as_view()),
    path('api/clients/<int:pk>/', api.GetClientApi.as_view()),
    path('api/clients/<int:pk>/primary_individual/', api.GetPrimaryIndividual.as_view()),
    path('api/tasks/client_task/<int:pk>/', api.UpdateClientTaskApi.as_view()),
    path('api/generation/individual_<int:pk>/all', api.GenerationGetAllApi.as_view()),
    path('api/generation/individual_<int:pk>/tasks', api.GenerationGetTasksApi.as_view()),
    url(r'clients_list', clients_list,name="clients_list"),
    url(r'users_list', users_list, name="users_list"),

    path(r'client_scoring/<int:id>/', client_scoring, name="client_scoring"),
    url(r'source', source, name="source"),
    path(r'client_inspect/<int:id>/',client_inspect,name="client_inspect")
]
