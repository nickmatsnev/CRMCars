import sys
import json

sys.path.append('../')

from core.lib import basic_api_requestor
from core.lib.constants import *


###     INDIVIDUALS     ###
def get_individual_info(id):
    path = URL_MAIN_INDIVIDUAL + f'{id}'
    return basic_api_requestor.request(path)

def get_individual_cur_data_source(id):
    path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_MAIN_SUB_CUR_DATA +URL_MODULE_SOURCE
    return basic_api_requestor.request(path)

def get_individual_cur_data_score(id):
    path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_MAIN_SUB_CUR_DATA +URL_MODULE_SCORING + URL_INDIVIDUAL_METHOD_SCORE
    return basic_api_requestor.request(path)

def get_individual_cur_data_parser_values(id):
        path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_MAIN_SUB_CUR_DATA + URL_MODULE_PARSER + URL_INDIVIDUAL_METHOD_VALUES
        return basic_api_requestor.request(path)

def get_individual_cur_data_parser_validate_errors(id):
    path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_MAIN_SUB_CUR_DATA + URL_MODULE_PARSER + URL_INDIVIDUAL_METHOD_VALIDATE_ERRORS
    return basic_api_requestor.request(path)

def get_individual_cur_data_parser_validate_status(id):
    path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_MAIN_SUB_CUR_DATA + URL_MODULE_PARSER + URL_INDIVIDUAL_METHOD_VALIDATE_STATUS
    return basic_api_requestor.request(path)

def get_individual_cur_data_parser_stopfactor_status(id):
    path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_MAIN_SUB_CUR_DATA + URL_MODULE_PARSER + URL_INDIVIDUAL_METHOD_STOP_STATUS
    return basic_api_requestor.request(path)

def get_individual_cur_data_parser_stopfactor_errors(id):
    path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_MAIN_SUB_CUR_DATA + URL_MODULE_PARSER + URL_INDIVIDUAL_METHOD_STOP_ERRORS
    return basic_api_requestor.request(path)

def do_individual_accept(id):
    path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_INDIVIDUAL_OPS_POST_ACCEPT
    return basic_api_requestor.request(path)

def do_individual_reject(id):
    path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_INDIVIDUAL_OPS_POST_REJECT
    return basic_api_requestor.request(path)

def do_individual_pre_reject(id):
    path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_INDIVIDUAL_OPS_PRE_REJECT
    return basic_api_requestor.request(path)

def do_individual_start(id):
    path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_INDIVIDUAL_OPS_START
    return basic_api_requestor.request(path)

def do_individual_next(id):
    path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_INDIVIDUAL_OPS_GEN_NEXT
    return basic_api_requestor.request(path)


###     MODULES     ###
def get_module_view(module_name):
    path = URL_MAIN_MODULE + f'{module_name}/' + URL_MODULE_METHOD_VIEW
    return basic_api_requestor.request(path)

def get_scoring_view():
    path = URL_MAIN_MODULE + URL_MODULE_SCORING + URL_MODULE_METHOD_VIEW
    return basic_api_requestor.request(path)

def do_module_upload(module_name,request):
    path = URL_MAIN_MODULE + f'{module_name}' + URL_MODULE_METHOD_UPLOAD
    return basic_api_requestor.post_file(path, request)

def get_module_parser_parameters():
    path = URL_MAIN_MODULE + URL_MODULE_PARSER + URL_MODULE_METHOD_VIEW_PARAMETERS
    return basic_api_requestor.request(path)

def get_module_parser_view():
    path = URL_MAIN_MODULE + URL_MODULE_PARSER + URL_MODULE_METHOD_VIEW
    return basic_api_requestor.request(path)


###     CLIENTS     ###
def get_client_view(id):
    path = URL_MAIN_CLIENT + f'{id}' + URL_CLIENT_METHOD_VIEW
    return basic_api_requestor.request(path)

def get_client_all():
    path = URL_MAIN_CLIENT
    return basic_api_requestor.request(path)

def get_client_all_status():
    path = URL_MAIN_CLIENT + URL_CLIENT_METHOD_STATUS
    return basic_api_requestor.request(path)

def get_client_by_status(status):
    path = URL_MAIN_CLIENT + status + '/'
    return basic_api_requestor.request(path)


###     PRODUCTS     ###
def post_product(data):
    path = URL_MAIN_PRODUCT
    return basic_api_requestor.post(path, data)

def patch_product(id,data):
    path = URL_MAIN_PRODUCT+f'{id}/'
    return basic_api_requestor.patch(path, data)

def get_product(id):
    path = URL_MAIN_PRODUCT + f'{id}'
    return basic_api_requestor.request(path)

def get_product_info():
    path = URL_MAIN_PRODUCT + URL_PRODUCT_METHOD_VIEW
    return basic_api_requestor.request(path)


###     USERS     ###
def _get_users():
    path = URL_MAIN_PRODUCT + URL_PRODUCT_METHOD_VIEW
    return basic_api_requestor.request(path)


### CLIENT PROCESSOR ###
def get_raw_willz(raw_willz_id):
    response = basic_api_requestor.request(URL_MAIN_WILLZ+f'{raw_willz_id}/')
    return response

def get_client_from_raw_willz(json_data):
    response = basic_api_requestor.post_decode(URL_MAIN_CLIENT,json_data)
    return response


def update_client_product(client_id,json_data):
    path = URL_MAIN_CLIENT + f'{id}/' + URL_CLIENT_UPDATE_PRODUCT
    return basic_api_requestor.post(path,json_data)


### PARSER PROCESSOR ###

def get_parser_body(parser):
    parser_body = basic_api_requestor.request(URL_MAIN_MODULE + URL_MODULE_PARSER + f'{parser}/')[0]
    return parser_body


def get_source_raw_data(individual_id,source_module_name):
    source_raw_data = basic_api_requestor.request(URL_MAIN_INDIVIDUAL + f'{individual_id}' +
                                                  URL_MAIN_SUB_CUR_DATA + URL_MODULE_SOURCE +f'{source_module_name}')
    return source_raw_data


def get_individual_json(individual_id):
    individual_json = basic_api_requestor.request(URL_MAIN_INDIVIDUAL+f'{individual_id}')
    return individual_json


def update_parser(individual_id,parser_m_name,parser_raw_data):
    response = basic_api_requestor.post(
            URL_MAIN_INDIVIDUAL+f'{individual_id}'+URL_MAIN_SUB_CUR_DATA+URL_MODULE_PARSER+f'{parser_m_name}/',
            parser_raw_data)
    return response


### SCORING PROCESSOR ###

def get_parser_method_values(individual_id):
    raw_data = basic_api_requestor.request(URL_MAIN_INDIVIDUAL + f'/{individual_id}'+ URL_MAIN_SUB_CUR_DATA
                                               +URL_MODULE_PARSER+URL_INDIVIDUAL_METHOD_VALUES)
    return raw_data


def update_scoring(individual_id, module_name,raw_data):
    response = basic_api_requestor.post(
            URL_MAIN_INDIVIDUAL + f'{individual_id}' + URL_MAIN_SUB_CUR_DATA
            + URL_MODULE_SCORING + f'{module_name}/', raw_data)
    return response


### SOURCES PROCESSOR ###
def get_source(source_name):
    source = basic_api_requestor.request(URL_MAIN_MODULE + URL_MODULE_SOURCE + f'{source_name}/')[0]
    return source


def update_source(individual_id, module_name,raw_data):
    response = basic_api_requestor.post(
                URL_MAIN_INDIVIDUAL + f'{individual_id}' + URL_MAIN_SUB_CUR_DATA
                + URL_MODULE_SOURCE  + f'{module_name}/',
                    raw_data)
    return response