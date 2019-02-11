import sys
sys.path.append('../')


from django.conf.urls import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers
from rest_framework import permissions
from django.urls import path

from web.portal.api import backend
from web.portal.api import frontend
from portal.controllers.views import *
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
router.register(r'api/willz', backend.RawClientDataApi)
# Работа с клиентскими данными
router.register(r'api/clients/new', backend.CreateClientApi)
#router.register(r'api/generation', api.GetGenerationApi)
router.register(r'api/individuals', backend.IndividualsApi)
router.register(r'api/passports', backend.PassportsApi)
router.register(r'api/driver_licenses', backend.DriverLicesesApi)
router.register(r'api/images', backend.ImagesApi)
router.register(r'api/clients', backend.ClientApi)
# Работа с генерацией
router.register(r'api/generation', backend.GenerationApi)
# Работа с фронтом
router.register(r'api/front/users', frontend.UserListApi)


urlpatterns = [
    url(r'^$', sign_in, name="signup"),
    url(r'^', include(router.urls)),

    url(r'^signup/$', sign_up, name='signup'),
    url(r'signin/$', sign_in, name="signin"),
    url(r'signout/$', sign_out, name="signout"),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/willz/', backend.WillzCreateClient.as_view()),
    path('api/new_action/', backend.NewActionApi.as_view()),
    path('api/bus_message/', backend.BusMessageAPI.as_view()),

# *** PARSER METHODS ***
    # backend
    path('api/back/parser_modules/<int:pk>/', backend.ParserGetAPI.as_view()),
    path('api/back/parser_modules/<int:pk>/activate/', backend.ParserActivateAPI.as_view()),
    path('api/back/parser_modules/<int:pk>/deactivate/', backend.ParserDeactivateAPI.as_view()),
    path('api/back/parser_modules/<int:pk>/parameters/', backend.ParserGetParametersAPI.as_view()),
    #frontend
    path('api/front/parser_modules/get_active_parsers_parameters/', frontend.ParserGetActiveAPI.as_view()),
    path('api/front/parser_modules/get_all_parsers/', frontend.ParserGetAllAPI.as_view()),
    path('api/front/parser_modules/upload_new_module/', frontend.ParserUploadAPI.as_view()),

# *** SCORING METHODS ***
    # backend
    path('api/back/scoring_modules/<int:pk>/', backend.ScoringGetAPI.as_view()),
    path('api/back/scoring_modules/<int:pk>/activate/', backend.ScoringActivateAPI.as_view()),
    path('api/back/scoring_modules/<int:pk>/deactivate/', backend.ScoringDeactivateAPI.as_view()),
    path('api/back/scoring_modules/<int:pk>/parameters/', backend.ScoringGetParametersAPI.as_view()),
    #frontend
    path('api/front/scoring_modules/get_active_scorings_parameters/', frontend.ScoringGetActiveAPI.as_view()),
    path('api/front/scoring_modules/get_all_scorings/', frontend.ScoringGetAllAPI.as_view()),
    path('api/front/scoring_modules/upload_new_module/', frontend.ScoringUploadAPI.as_view()),

# *** SOURCE METHODS ***
    # backend
    path('api/back/source_modules/<int:pk>/', backend.SourceGetAPI.as_view()),
    path('api/back/source_modules/<int:pk>/activate/', backend.SourceActivateAPI.as_view()),
    path('api/back/source_modules/<int:pk>/deactivate/', backend.SourceDeactivateAPI.as_view()),
    path('api/back/source_modules/<int:pk>/parameters/', backend.SourceGetParametersAPI.as_view()),
    #frontend
    path('api/front/source_modules/get_active_sourcess_parameters/', frontend.SourceGetActiveAPI.as_view()),
    path('api/front/source_modules/get_all_sources/', frontend.SourceGetAllAPI.as_view()),
    path('api/front/source_modules/upload_new_module/', frontend.SourceUploadAPI.as_view()),

    path('api/front/clients/', frontend.ClientsListApi.as_view()),
    path('api/front/clients/<int:pk>/', frontend.ClientInspectApi.as_view()),

    url(r'clients_list', clients_list,name="clients_list"),
    url(r'users_list', users_list, name="users_list"),
    url(r'parameters_list', parameters_list, name="parameters_list"),

    path(r'client_scoring/<int:id>/', client_scoring, name="client_scoring"),
    path(r'accept_client/<int:id>/', accept_client, name="accept_client"),
    path(r'reject_client/<int:id>/', reject_client, name="reject_client"),

    url(r'source', source, name="source"),
    path(r'client_inspect/<int:id>/',client_inspect,name="client_inspect"),
    path(r'client_decline/<int:id>/',client_decline,name="client_decline"),

    url(r'upload_parser_module', upload_parser_module, name="upload_parser_module")


]
