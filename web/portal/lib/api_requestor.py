from core.lib import basic_api_requestor
from portal.lib.constants import *

###     INDIVIDUALS     ###
def get_individual_info(id):
    path = URL_MAIN_INDIVIDUAL + f'/{id}'
    return basic_api_requestor.request(path)


def get_individual_cur_data_info(id,module_name,command=''):
    path = URL_MAIN_INDIVIDUAL + f'/{id}' + URL_MAIN_SUB_CUR_DATA + f'/{module_name}'
    if (command != ''):
        path += f'{command}'

    return basic_api_requestor.request(path)


def do_individual_ops(id,operation):
    path = URL_MAIN_INDIVIDUAL + f'/{id}' + URL_MAIN_SUB_INDIVIDUAL_OPS + f'/{operation}'

    return basic_api_requestor.request(path)


###     MODULES     ###
def get_module_info(module_name,command=''):
    path = URL_MAIN_MODULE + f'/{module_name}'
    if (command != ''):
        path += f'{command}'

    return basic_api_requestor.request(path)


def do_module_upload(module_name,request):
    path = URL_MAIN_MODULE + f'/{module_name}'+URL_MODULE_METHOD_UPLOAD
    return basic_api_requestor.post_file(path, request)


###     CLIENTS     ###
def get_client(command=''):
    path = URL_MAIN_CLIENT + '/'
    if (command!=''):
        path += command
    return basic_api_requestor.request(path)


def get_client_info(id,command=''):
    path = URL_MAIN_CLIENT + f'/{id}'
    if (command != ''):
        path += f'/{command}'

    return basic_api_requestor.request(path)


###     PRODUCTS     ###
def post_product(data):
    path = URL_MAIN_PRODUCT+'/'
    return basic_api_requestor.post('/product/', data)


def patch_product(id,data):
    path = URL_MAIN_PRODUCT+f'/{id}/'
    return basic_api_requestor.patch('/product/', data)


def get_product(id):
    path = URL_MAIN_PRODUCT + f'/{id}'
    return basic_api_requestor.request(path)


def get_product_info():
    path = URL_MAIN_PRODUCT +'/'+ URL_PRODUCT_METHOD_VIEW
    return basic_api_requestor.request(path)


###     USERS     ###
def get_users():
    path = URL_MAIN_PRODUCT +'/'+ URL_PRODUCT_METHOD_VIEW
    return basic_api_requestor.request(path)

