import sys

from django.conf.urls.static import static
from django.views.decorators.cache import never_cache
from django.views.static import serve

from portal import settings

sys.path.append('../')

from django.conf.urls import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers
from rest_framework import permissions
from django.urls import path
import json
from portal.api import api_client
from portal.api import api_willz
from portal.api import api_user
from portal.api import api_message
from portal.api import api_module
from portal.api import api_product
from portal.api import api_individual
from portal.api import api_status

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


#router.register(r'api/client', api_client.MainAPI)
router.register(r'api/willz', api_willz.MainAPI)
router.register(r'api/user', api_user.MainAPI)
router.register(r'api/product', api_product.MainAPI)
#router.register(r'api/individual/<int:pk>/data/parser/<slug:module_name>',api_module.GetParserInfoAPI)
#router.register(r'api/individual',api_module.GetScoringInfoAPI)

#reformat:

#POST api/client/ - кидаем структурированного клиента полного, создаем и генерацию и продукты и проч
#GET  api/client/ - получаем сырые данные из базы
#PUT  api/client/ - отправляем структурированного полного клиента с целью обновления
#GET  api/client/fields - получаем доступные поля из базы
#POST api/client/view - отправляем параметры, которые нужны, получаем табличку для HTML
#GET  api/client/<id>/ - получаем конкретного сырого клиента
#POST api/client/<id>/view - получаем конкретного клиента по полям, которые отправили
#POST api/client/<id>/action - добавляем новое действие для клиента
#POST api/client/<id>/update - меняем данные по связке поле:значение


#POST api/willz/   - отправляем любое г от виллза
#POST api/willz/update   - отправляем любое обновление для г от виллза, айди берем вилзовское изнутри и ищем совпадение
#GET  api/willz/<id> - получаем обратно любое г от виллза


#POST api/message/ - отправляем новое сообщение
#GET  api/message/ - получаем все сообщения со статусом доставки !!!под вопросом - нужо ли??? !!!!


#GET  api/module/<type>/ 	- получить модули со всеми типами
#POST api/module/<type>/upload   - загрузить новый модуль
#GET  api/module/parser/parameters 	- получить все активные параметры парсера

#GET  api/module/<type>/<id> 	- получить конкретный модуль
#GET  api/module/<type>/<id>/activate 	- включить
#GET  api/module/<type>/<id>/deactivate 	- выключить

urlpatterns = [

    url(r'^$', sign_in, name="signup"),
    url(r'^', include(router.urls)),

    url(r'^signup/$', sign_up, name='signup'),
    url(r'signin/$', sign_in, name="signin"),
    url(r'signout/$', sign_out, name="signout"),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/message/', api_message.MainApi.as_view()),
    path('api/status/', api_status.MainApi.as_view()),
    path('api/test/', api_message.TestApi.as_view()),

    path('api/client/', api_client.ClientApi.as_view()),
    path('api/client/status/', api_client.ClientGetStatusApi.as_view()),
    path('api/client/<slug:filter_status>/', api_client.ClientFilterApi.as_view()),
    path('api/client/<int:id>', api_client.ClientWorkApi.as_view()),
    path('api/client/<int:id>/update_product/', api_client.UpdateProductApi.as_view()),

    path('api/module/<slug:module_type>/', api_module.GetModuleApi.as_view()),
    path('api/module/<slug:module_type>/view/', api_module.ViewModuleApi.as_view()),
    path('api/module/<slug:module_type>/view/parameters/', api_module.GetViewParametersApi.as_view()),
    path('api/module/<slug:module_type>/upload/', api_module.UploadModuleApi.as_view()),
    path('api/module/<slug:module_type>/<slug:module_name>/delete/', api_module.DeleteModuleApi.as_view()),

    path('api/module/<slug:module_type>/<int:pk>/', api_module.GetModuleByIdApi.as_view()),
    path('api/module/<slug:module_type>/<slug:module_name>/', api_module.GetModuleByNameApi.as_view()),

    path('api/module/<slug:module_type>/<int:id>/parameters/', api_module.GetModuleParametersByIdApi.as_view()),
    path('api/module/<slug:module_type>/<int:id>/activate/', api_module.ActivateApi.as_view()),
    path('api/module/<slug:module_type>/<int:id>/deactivate/', api_module.DeactivateApi.as_view()),

    path('api/module/source/<int:id>/credentials/', api_module.CredentialsApi.as_view()),

    path('api/individual/<int:pk>',
         api_individual.MainApi.as_view()),
    path('api/individual/<int:pk>/ops/postscoring_reject/',
         api_status.PostReject.as_view()),
    path('api/individual/<int:pk>/ops/postscoring_accept/',
         api_status.PostAccept.as_view()),
    path('api/individual/<int:pk>/ops/prescoring_reject/',
         api_status.PreReject.as_view()),
    path('api/individual/<int:pk>/ops/scoring_start/',
         api_status.ScoringStart.as_view()),
    path('api/individual/<int:pk>/ops/generation_next/',
         api_individual.NewGenApi.as_view()),
    path('api/individual/<int:pk>/current_generation/',
         api_individual.CurGenApi.as_view()),
    path('api/individual/<int:pk>/current_generation/state/',
         api_individual.CurGenStateApi.as_view()),
    path('api/individual/<int:pk>/generations/',
         api_individual.GenApi.as_view()),
    path('api/individual/<int:pk>/<slug:gen_id_or_cur_gen>/add_action/',
         api_individual.AddActionApi.as_view()),
    path('api/individual/<int:pk>/<slug:gen_id_or_cur_gen>/data/parser/values/',
         api_module.GetAllParserValuesAPI.as_view()),

    path('api/individual/<int:pk>/<slug:gen_id_or_cur_gen>/data/scoring/<slug:module_name>/score/',
         api_module.GetScoringAPI.as_view()),
    path('api/individual/<int:pk>/<slug:gen_id_or_cur_gen>/data/scoring/score/',
         api_module.GetAllScoringAPI.as_view()),

    path('api/individual/<int:pk>/<slug:gen_id_or_cur_gen>/data/parser/<slug:module_name>/validate_status/',
         api_module.GetParserValidateStatusAPI.as_view()),
    path('api/individual/<int:pk>/<slug:gen_id_or_cur_gen>/data/parser/<slug:module_name>/validate_errors/',
         api_module.GetParserValidateErrorsAPI.as_view()),
    path('api/individual/<int:pk>/<slug:gen_id_or_cur_gen>/data/parser/<slug:module_name>/stopfactor_status/',
         api_module.GetParserStopFactorStatusAPI.as_view()),
    path('api/individual/<int:pk>/<slug:gen_id_or_cur_gen>/data/parser/<slug:module_name>/stopfactor_errors/',
         api_module.GetParserStopFactorErrorsAPI.as_view()),

    path('api/individual/<int:pk>/<slug:gen_id_or_cur_gen>/data/parser/<slug:module_name>/values/',
         api_module.GetParserValuesAPI.as_view()),

    path('api/individual/<int:pk>/<slug:gen_id_or_cur_gen>/data/parser/validate/errors/',
         api_module.GetParserValidateAllErrorsAPI.as_view()),
    path('api/individual/<int:pk>/<slug:gen_id_or_cur_gen>/data/parser/stopfactor/errors/',
         api_module.GetParserStopFactorAllErrorsAPI.as_view()),

    path('api/individual/<int:pk>/<slug:gen_id_or_cur_gen>/data/<slug:module_type>/<slug:module_name>/',
         api_module.ModuleDataApi.as_view()),
    path('api/individual/<int:pk>/<slug:gen_id_or_cur_gen>/data/<slug:module_type>/<slug:module_name>/meta/',
         api_module.ModuleMetaApi.as_view()),
    path('api/individual/<int:pk>/<slug:gen_id_or_cur_gen>/data/<slug:module_type>/',
         api_module.ModuleDataListApi.as_view()),



    url(r'clients_list', clients_list,name="clients_list"),
    url(r'users_list', users_list, name="users_list"),
    url(r'parameters_list', parameters_list, name="parameters_list"),
    url(r'products_list', products_list, name="products_list"),

    path(r'modules_list/<slug:module_type>/', modules_list, name="modules_list"),

    path(r'individual_scoring/<int:id>/', individual_scoring, name="individual_scoring"),
    path(r'accept_individual/<int:id>/', accept_individual, name="accept_individual"),
    path(r'reject_individual/<int:id>/', reject_individual, name="reject_individual"),

    path(r'individual_inspect/<int:id>/', individual_inspect, name="individual_inspect"),
    path(r'individual_prescoring_decline/<int:id>/', individual_prescoring_decline,
         name="individual_prescoring_decline"),

    path(r'product_edit/<int:id>/', product_edit, name="product_edit"),
    path(r'product_new/', product_new, name="product_new"),

    path(r'upload_module/<slug:module_type>/', upload_module, name="upload_module"),

]

urlpatterns += static(settings.STATIC_URL, view=never_cache(serve))
