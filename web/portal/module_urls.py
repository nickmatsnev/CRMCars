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


urlpatterns = [
    path(r'<slug:module_type>/', api_module.GetModuleApi.as_view()),
    path(r'<slug:module_type>/' + f'{NAME_VIEW}/', api_module.ViewModuleApi.as_view()),
    path(r'<slug:module_type>/' + f'{NAME_VIEW}/{NAME_PARAMETERS}/', api_module.GetViewParametersApi.as_view()),
    path(r'<slug:module_type>/' + f'{NAME_UPLOAD}/', api_module.UploadModuleApi.as_view()),
    path(r'<slug:module_type>/' + r'<slug:module_name>/' +f'{NAME_DELETE}/', api_module.DeleteModuleApi.as_view()),

    path(r'<slug:module_type>/' + r'<int:pk>/', api_module.GetModuleByIdApi.as_view()),
    path(r'<slug:module_type>/' + r'<slug:module_name>/', api_module.GetModuleByNameApi.as_view()),

    path(r'<slug:module_type>/' + r'<int:id>/' + f'{NAME_PARAMETERS}/', api_module.GetModuleParametersByIdApi.as_view()),
    path(r'<slug:module_type>/' + r'<int:id>/' + f'{NAME_PARAMETERS}/' + f'{NAME_ACTIVATE}/', api_module.ActivateApi.as_view()),
    path(r'<slug:module_type>/' + r'<int:id>/' + f'{NAME_PARAMETERS}/' + f'{NAME_DEACTIVATE}/', api_module.DeactivateApi.as_view()),

    path(f'/{NAME_SOURCE}/'+r'<int:id>/' + f'{NAME_CREDENTIALS}/', api_module.CredentialsApi.as_view())
]