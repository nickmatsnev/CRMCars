import sys

sys.path.append('../')

from core.lib import basic_api_requestor
from core.lib.constants import *


###     INDIVIDUALS     ###
def get_individual_info(id):
    path = URL_MAIN_INDIVIDUAL + f'/{id}'
    return basic_api_requestor.request(path)

def get_individual_cur_data_source(id):
    path = URL_MAIN_INDIVIDUAL + f'/{id}' + URL_MAIN_SUB_CUR_DATA + f'/'+URL_MODULE_SOURCE
    return basic_api_requestor.request(path)

def get_individual_cur_data_score(id):
    path = URL_MAIN_INDIVIDUAL + f'/{id}' + URL_MAIN_SUB_CUR_DATA + f'/'+URL_MODULE_SCORING + URL_INDIVIDUAL_METHOD_SCORE
    return basic_api_requestor.request(path)

def get_individual_cur_data_parser_values(id):
        path = URL_MAIN_INDIVIDUAL + f'/{id}' + URL_MAIN_SUB_CUR_DATA + f'/' + URL_MODULE_PARSER + URL_INDIVIDUAL_METHOD_VALUES
        return basic_api_requestor.request(path)

def get_individual_cur_data_parser_validate_errors(id):
    path = URL_MAIN_INDIVIDUAL + f'/{id}' + URL_MAIN_SUB_CUR_DATA + f'/' + URL_MODULE_PARSER + URL_INDIVIDUAL_METHOD_VALIDATE_ERRORS
    return basic_api_requestor.request(path)

def get_individual_cur_data_parser_validate_status(id):
    path = URL_MAIN_INDIVIDUAL + f'/{id}' + URL_MAIN_SUB_CUR_DATA + f'/' + URL_MODULE_PARSER + URL_INDIVIDUAL_METHOD_VALIDATE_STATUS
    return basic_api_requestor.request(path)

def get_individual_cur_data_parser_stopfactor_status(id):
    path = URL_MAIN_INDIVIDUAL + f'/{id}' + URL_MAIN_SUB_CUR_DATA + f'/' + URL_MODULE_PARSER + URL_INDIVIDUAL_METHOD_STOP_STATUS
    return basic_api_requestor.request(path)

def get_individual_cur_data_parser_stopfactor_errors(id):
    path = URL_MAIN_INDIVIDUAL + f'/{id}' + URL_MAIN_SUB_CUR_DATA + f'/' + URL_MODULE_PARSER + URL_INDIVIDUAL_METHOD_STOP_ERRORS
    return basic_api_requestor.request(path)

def do_individual_accept(id):
    path = URL_MAIN_INDIVIDUAL + f'/{id}' + URL_MAIN_SUB_INDIVIDUAL_OPS + f'/' + URL_INDIVIDUAL_OPS_POST_ACCEPT
    return basic_api_requestor.request(path)

def do_individual_reject(id):
    path = URL_MAIN_INDIVIDUAL + f'/{id}' + URL_MAIN_SUB_INDIVIDUAL_OPS + f'/' + URL_INDIVIDUAL_OPS_POST_REJECT
    return basic_api_requestor.request(path)

def do_individual_pre_reject(id):
    path = URL_MAIN_INDIVIDUAL + f'/{id}' + URL_MAIN_SUB_INDIVIDUAL_OPS + f'/' + URL_INDIVIDUAL_OPS_PRE_REJECT
    return basic_api_requestor.request(path)

def do_individual_start(id):
    path = URL_MAIN_INDIVIDUAL + f'/{id}' + URL_MAIN_SUB_INDIVIDUAL_OPS + f'/' + URL_INDIVIDUAL_OPS_START
    return basic_api_requestor.request(path)

def do_individual_next(id):
    path = URL_MAIN_INDIVIDUAL + f'/{id}' + URL_MAIN_SUB_INDIVIDUAL_OPS + f'/' + URL_INDIVIDUAL_OPS_GEN_NEXT
    return basic_api_requestor.request(path)


###     MODULES     ###
def get_module_view(module_name):
    path = URL_MAIN_MODULE + f'/{module_name}/' + URL_MODULE_METHOD_VIEW
    return basic_api_requestor.request(path)

def get_scoring_view():
    path = URL_MAIN_MODULE + f'/' + URL_MODULE_SCORING + URL_MODULE_METHOD_VIEW
    return basic_api_requestor.request(path)

def do_module_upload(module_name,request):
    path = URL_MAIN_MODULE + f'/{module_name}/' + URL_MODULE_METHOD_UPLOAD
    return basic_api_requestor.post_file(path, request)

def get_module_parser_parameters():
    path = URL_MAIN_MODULE + f'/' + URL_MODULE_PARSER + URL_MODULE_METHOD_VIEW_PARAMETERS
    return basic_api_requestor.request(path)

def get_module_parser_view():
    path = URL_MAIN_MODULE + f'/' + URL_MODULE_PARSER + URL_MODULE_METHOD_VIEW
    return basic_api_requestor.request(path)


###     CLIENTS     ###
def get_client_view(id):
    path = URL_MAIN_CLIENT + f'/{id}/' + URL_CLIENT_METHOD_VIEW
    return basic_api_requestor.request(path)

def get_client_all():
    path = URL_MAIN_CLIENT + '/'
    return basic_api_requestor.request(path)

def get_client_all_status():
    path = URL_MAIN_CLIENT + '/' + URL_CLIENT_METHOD_STATUS
    return basic_api_requestor.request(path)

def get_client_by_status(status):
    path = URL_MAIN_CLIENT + '/' + status + '/'
    return basic_api_requestor.request(path)


###     PRODUCTS     ###
def post_product(data):
    path = URL_MAIN_PRODUCT+'/'
    return basic_api_requestor.post(path, data)

def patch_product(id,data):
    path = URL_MAIN_PRODUCT+f'/{id}/'
    return basic_api_requestor.patch(path, data)

def get_product(id):
    path = URL_MAIN_PRODUCT + f'/{id}'
    return basic_api_requestor.request(path)

def get_product_info():
    path = URL_MAIN_PRODUCT +'/'+ URL_PRODUCT_METHOD_VIEW
    return basic_api_requestor.request(path)


###     USERS     ###
def _get_users():
    path = URL_MAIN_PRODUCT +'/'+ URL_PRODUCT_METHOD_VIEW
    return basic_api_requestor.request(path)

