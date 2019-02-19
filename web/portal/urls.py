import sys
sys.path.append('../')

from django.conf.urls import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers
from rest_framework import permissions
from django.urls import path

from portal.api import api_client
from portal.api import api_willz
from portal.api import api_user
from portal.api import api_message
from portal.api import api_module

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


router.register(r'api/client', api_client.MainAPI)
router.register(r'api/willz', api_willz.MainAPI)
router.register(r'api/user', api_user.MainAPI)

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

    path('api/module/<slug:module_type>/', api_module.GetModuleApi.as_view()),
    path('api/module/<slug:module_type>/view/', api_module.UploadModuleApi.as_view()),
    path('api/module/<slug:module_type>/view/parameters/', api_module.GetViewParametersApi.as_view()),
    path('api/module/<slug:module_type>/upload/', api_module.UploadModuleApi.as_view()),


    path('api/module/<slug:module_type>/<int:id>/', api_module.GetModuleByIdApi.as_view()),
    path('api/module/<slug:module_type>/<int:id>/parameters/', api_module.GetModuleParametersByIdApi.as_view()),
    path('api/module/<slug:module_type>/<int:id>/activate/', api_module.ActivateApi.as_view()),
    path('api/module/<slug:module_type>/<int:id>/deactivate/', api_module.DeactivateApi.as_view()),


    url(r'clients_list', clients_list,name="clients_list"),
    url(r'users_list', users_list, name="users_list"),
    url(r'parameters_list', parameters_list, name="parameters_list"),

    path(r'modules_list/<slug:module_type>/', modules_list, name="modules_list"),

    path(r'client_scoring/<int:id>/', client_scoring, name="client_scoring"),
    path(r'accept_client/<int:id>/', accept_client, name="accept_client"),
    path(r'reject_client/<int:id>/', reject_client, name="reject_client"),


    path(r'client_inspect/<int:id>/',client_inspect,name="client_inspect"),
    path(r'client_decline/<int:id>/',client_decline,name="client_decline"),

    path(r'upload_module/<slug:module_type>/', upload_module, name="upload_module"),

]
