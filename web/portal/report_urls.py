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
from portal.api import api_report


from portal.controllers.views import *
from portal.controllers.individual_view import *
from portal.controllers.module_view import *
from .controllers.auth import *


urlpatterns = [
    path(f'{NAME_GENERAL}/', api_report.GeneralReport.as_view()),
    path(f'{NAME_ADVANCED}/', api_report.AdvancedReport.as_view()),
]