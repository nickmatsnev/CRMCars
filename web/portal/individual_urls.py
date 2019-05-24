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
    path('',         api_individual.MainApi.as_view()),
    path(f'/{NAME_OPS}/{NAME_POSTSCORING_REJECT}/',         api_status.PostReject.as_view()),
    path(f'/{NAME_OPS}/{NAME_POSTSCORING_ACCEPT}/',         api_status.PostAccept.as_view()),
    path(f'/{NAME_OPS}/{NAME_PRESCORING_REJECT}/',         api_status.PreReject.as_view()),
    path(f'/{NAME_OPS}/{NAME_SCORING_START}/',         api_status.ScoringStart.as_view()),
    path(f'/{NAME_OPS}/{NAME_GENERATION_NEXT}/',         api_individual.NewGenApi.as_view()),
    path(f'/{NAME_CURRENT_GENERATION}/',         api_individual.CurGenApi.as_view()),
    path(f'/{NAME_CURRENT_GENERATION}/{NAME_STATE}/',         api_individual.CurGenStateApi.as_view()),
    path(f'/{NAME_GENERATIONS}/',         api_individual.GenApi.as_view()),
    path(r'/<slug:gen_id_or_cur_gen>/' + f'{NAME_ADD_ACTION}/',         api_individual.AddActionApi.as_view()),
    path(r'/<slug:gen_id_or_cur_gen>/' + f'{NAME_DATA}/{NAME_PARSER}/{NAME_VALUES}/',         api_module.GetAllParserValuesAPI.as_view()),

    path(r'/<slug:gen_id_or_cur_gen>/' + f'{NAME_DATA}/{NAME_SCORING}/' + r'<slug:module_name>/' + f'{NAME_SCORE}/',         api_module.GetScoringAPI.as_view()),
    path(r'/<slug:gen_id_or_cur_gen>/' + f'{NAME_DATA}/{NAME_SCORING}/' + f'{NAME_SCORE}/',         api_module.GetAllScoringAPI.as_view()),

    path(r'/<slug:gen_id_or_cur_gen>/' + f'{NAME_DATA}/{NAME_PARSER}/' + r'<slug:module_name>/' + f'{NAME_VALIDATE_STATUS}/',         api_module.GetParserValidateStatusAPI.as_view()),
    path(r'/<slug:gen_id_or_cur_gen>/' + f'{NAME_DATA}/{NAME_PARSER}/' + r'<slug:module_name>/' + f'{NAME_VALIDATE_ERRORS}/',         api_module.GetParserValidateErrorsAPI.as_view()),
    path(r'/<slug:gen_id_or_cur_gen>/' + f'{NAME_DATA}/{NAME_PARSER}/' + r'<slug:module_name>/' + f'{NAME_STOPFACTOR_STATUS}/',         api_module.GetParserStopFactorStatusAPI.as_view()),
    path(r'/<slug:gen_id_or_cur_gen>/' + f'{NAME_DATA}/{NAME_PARSER}/' + r'<slug:module_name>/' + f'{NAME_STOPFACTOR_ERRORS}/',         api_module.GetParserStopFactorErrorsAPI.as_view()),

    path(r'/<slug:gen_id_or_cur_gen>/' + f'{NAME_DATA}/{NAME_PARSER}/' + r'<slug:module_name>/' + f'{NAME_VALUES}/',         api_module.GetParserValuesAPI.as_view()),

    path(r'/<slug:gen_id_or_cur_gen>/' + f'{NAME_DATA}/{NAME_PARSER}/{NAME_VALIDATE}/{NAME_ERRORS}/',         api_module.GetParserValidateAllErrorsAPI.as_view()),
    path(r'/<slug:gen_id_or_cur_gen>/' + f'{NAME_DATA}/{NAME_PARSER}/{NAME_STOPFACTOR}/{NAME_ERRORS}/',         api_module.GetParserStopFactorAllErrorsAPI.as_view()),
    path(r'/<slug:gen_id_or_cur_gen>/' + f'{NAME_DATA}/{NAME_PARSER}/{NAME_VALIDATE}/{NAME_STATUS}/',         api_module.GetParserValidateAllStatusAPI.as_view()),
    path(r'/<slug:gen_id_or_cur_gen>/' + f'{NAME_DATA}/{NAME_PARSER}/{NAME_STOPFACTOR}/{NAME_STATUS}/',         api_module.GetParserStopFactorAllStatusAPI.as_view()),

    path(r'/<slug:gen_id_or_cur_gen>/' + f'{NAME_DATA}/'+r'<slug:module_type>/<slug:module_name>/',         api_module.ModuleDataApi.as_view()),
    path(r'/<slug:gen_id_or_cur_gen>/' + f'{NAME_DATA}/'+r'<slug:module_type>/<slug:module_name>/'+ f'{NAME_META}/',         api_module.ModuleMetaApi.as_view()),
    path(r'/<slug:gen_id_or_cur_gen>/' + f'{NAME_DATA}/'+r'<slug:module_type>/',         api_module.ModuleDataListApi.as_view()),
]

