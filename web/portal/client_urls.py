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
    path('', api_client.ClientApi.as_view()),
    path(f'{NAME_STATUS}/', api_client.ClientGetStatusApi.as_view()),
    path(r'<str:filter_status_or_surname>/', api_client.ClientFilterApi.as_view()),
    path(r'<int:id>/', api_client.ClientWorkApi.as_view()),
    path(r'<int:id>/' + f'{NAME_UPDATE}/', api_client.UpdateClientWorkApi.as_view()),
    path(r'<int:id>/' + f'{NAME_UPDATE_PRODUCT}/', api_client.UpdateProductApi.as_view())
    ]