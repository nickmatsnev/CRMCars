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
from portal.controllers.individual_view import *
from portal.controllers.module_view import *
from .controllers.auth import *

router = routers.DefaultRouter()
view_router = routers.APIRootView()

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

# router.register(r'api/client', api_client.MainAPI)
router.register(f'{NAME_API}/{NAME_WILLZ}', api_willz.MainAPI)
router.register(f'{NAME_API}/{NAME_USER}', api_user.MainAPI)
router.register(f'{NAME_API}/{NAME_PRODUCT}', api_product.MainAPI)
# router.register(r'api/individual/<int:pk>/data/parser/<slug:module_name>',api_module.GetParserInfoAPI)
# router.register(r'api/individual',api_module.GetScoringInfoAPI)

# reformat:

# POST api/client/ - кидаем структурированного клиента полного, создаем и генерацию и продукты и проч
# GET  api/client/ - получаем сырые данные из базы
# PUT  api/client/ - отправляем структурированного полного клиента с целью обновления
# GET  api/client/fields - получаем доступные поля из базы
# POST api/client/view - отправляем параметры, которые нужны, получаем табличку для HTML
# GET  api/client/<id>/ - получаем конкретного сырого клиента
# POST api/client/<id>/view - получаем конкретного клиента по полям, которые отправили
# POST api/client/<id>/action - добавляем новое действие для клиента
# POST api/client/<id>/update - меняем данные по связке поле:значение


# POST api/willz/   - отправляем любое г от виллза
# POST api/willz/update   - отправляем любое обновление для г от виллза, айди берем вилзовское изнутри и ищем совпадение
# # GET  api/willz/<id> - получаем обратно любое г от виллза
#
#
# # POST api/message/ - отправляем новое сообщение
# # GET  api/message/ - получаем все сообщения со статусом доставки !!!под вопросом - нужо ли??? !!!!
#
#
# # GET  api/module/<type>/ 	- получить модули со всеми типами
# # POST api/module/<type>/upload   - загрузить новый модуль
# # GET  api/module/parser/parameters 	- получить все активные параметры парсера
#
# # GET  api/module/<type>/<id> 	- получить конкретный модуль
# # GET  api/module/<type>/<id>/activate 	- включить
# GET  api/module/<type>/<id>/deactivate 	- выключить

urlpatterns = [

    url(r'^$', sign_in, name="signup"),
    url(r'^', include(router.urls)),

    url(r'^signup/$', sign_up, name='signup'),
    url(r'signin/$', sign_in, name="signin"),
    url(r'signout/$', sign_out, name="signout"),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path(f'{NAME_API}/{NAME_MESSAGE}/', api_message.MainApi.as_view()),
    path(f'{NAME_API}/{NAME_STATUS}/', api_status.MainApi.as_view()),
    path(f'{NAME_API}/test/', api_message.TestApi.as_view()),

    path(f'{NAME_API}/{NAME_CLIENT}/', include('portal.client_urls')),
    path(f'{NAME_API}/{NAME_MODULE}/', include('portal.module_urls')),
    path(f'{NAME_API}/{NAME_REPORT}/', include('portal.report_urls')),

    path(f'{NAME_API}/{NAME_INDIVIDUAL}/' + r'<int:pk>', include('portal.individual_urls')),

    path(f'{NAME_CLIENTS_LIST}/' + r'<slug:status_filter>/', clients_list_filtered,
         name=NAME_CLIENTS_LIST + '_' + NAME_FILTERED),
    url(f'{NAME_CLIENTS_LIST}', clients_list, name=NAME_CLIENTS_LIST),
    url(f'{NAME_INDEX}', index, name=NAME_INDEX),

    url(f'{NAME_USERS_LIST}', users_list, name=NAME_USERS_LIST),
    url(f'{NAME_PARAMETERS_LIST}', parameters_list, name=NAME_PARAMETERS_LIST),
    url(f'{NAME_PRODUCTS_LIST}', products_list, name=NAME_PRODUCTS_LIST),
    url(f'{NAME_REPORTS}', reports, name=NAME_REPORTS),

    path(f'{NAME_MODULES_LIST}' + r'/<slug:module_type>/', modules_list, name=NAME_MODULES_LIST),

    path(f'{NAME_INDIVIDUAL_SCORING}/' + r'<int:id>/', individual_scoring, name=NAME_INDIVIDUAL_SCORING),
    path(f'{NAME_INDIVIDUAL_REPORT}/' + r'<int:id>/', individual_report, name=NAME_INDIVIDUAL_REPORT),
    path(f'{NAME_ACCEPT_INDIVIDUAL}/' + r'<int:id>/', accept_individual, name=NAME_ACCEPT_INDIVIDUAL),
    path(f'{NAME_REJECT_INDIVIDUAL}/' + r'<int:id>/', reject_individual, name=NAME_REJECT_INDIVIDUAL),
    path(f'{NAME_START_INDIVIDUAL_SCORING}/' + r'<int:id>/', start_individual_scoring,
         name=NAME_START_INDIVIDUAL_SCORING),
    path(f'{NAME_INDIVIDUAL_INSPECT}/' + r'<int:id>/', individual_inspect, name=NAME_INDIVIDUAL_INSPECT),
    path(f'{NAME_INDIVIDUAL_PRESCORING_DECLINE}/' + r'<int:id>/', individual_prescoring_decline,
         name=NAME_INDIVIDUAL_PRESCORING_DECLINE),
    path(f'{NAME_INDIVIDUAL_NEW_GENERATION}/' + r'<int:id>/', individual_new_generation,
         name=NAME_INDIVIDUAL_NEW_GENERATION),
    path(f'{NAME_INDIVIDUAL_OPERATIONS}/' + r'<int:id>/', individual_operations,
         name=NAME_INDIVIDUAL_OPERATIONS),

    path(f'{NAME_PRODUCT_EDIT}/' + r'<int:id>/', product_edit, name=NAME_PRODUCT_EDIT),
    path(f'{NAME_PRODUCT_NEW}/', product_new, name=NAME_PRODUCT_NEW),

    path(f'{NAME_UPLOAD_MODULE}/' + r'<slug:module_type>/', upload_module, name=NAME_UPLOAD_MODULE),

]

urlpatterns += static(settings.STATIC_URL, view=never_cache(serve))
