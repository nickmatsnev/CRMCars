import json
import traceback

import django
import requests
import socket

import os
import django
import sys

sys.path.append('../../')
sys.path.append('../../web')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.portal.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

from core.lib import constants
from core.lib.global_settings import *
from core.lib.constants import *



class ApiRequestor:
    __session = None
    __csrfToken = None
    __headers = {'Content-type': 'application/json'}

    def __init__(self, request=None):
        if (request is not None):
            self.__session = request.session.session_key
            self.__csrfToken = request.COOKIES.get('csrftoken')
        else:
            client = requests.session()
            url_login = LOGIN_ROOT_URL
            client.get(url_login)
            csrftoken = client.cookies['csrftoken']
            login_data = {'username': constants.ADMIN_USERNAME, 'password': constants.ADMIN_PASSWORD,
                              'csrfmiddlewaretoken': csrftoken}

            r1 = client.post(url_login, data=login_data, allow_redirects=False)

            self.__session = client.cookies['sessionid']
            self.__csrfToken = csrftoken

    def __prepare_auth_cookies(self):
        return {'csrftoken': self.__csrfToken, 'sessionid': self.__session}

    def __prepare_headers(self):
        return {'Content-type': 'application/json', 'X-CSRFToken': self.__csrfToken}

    def __prepare_general_headers(self):
        return {'X-CSRFToken': self.__csrfToken}

    def __get(self, relative_url):
        print("API_requestor:{0}".format(relative_url))
        cookies = self.__prepare_auth_cookies()
        response = requests.get(API_ROOT_URL + relative_url, cookies=self.__prepare_auth_cookies(),
                                headers=self.__prepare_headers())
        print("API_result:{0}".format(response.status_code))
        return json.loads(response.content.decode('utf-8'))

    def __post_decode(self, relative_url, body):
        print("API_requestor:{0}".format(relative_url))
        response = requests.post(API_ROOT_URL + relative_url, data=body, headers=self.__prepare_headers(),
                                 cookies=self.__prepare_auth_cookies())
        print("API_result:{0}".format(response.status_code))
        return json.loads(response.content.decode('utf-8'))

    def __post_file(self, relative_url, request):
        print("API_requestor:{0}".format(relative_url))
        file = request.FILES['file']
        files = {'file': file.open()}
        response = requests.post(API_ROOT_URL + relative_url, files=files, cookies=self.__prepare_auth_cookies(),
                                 headers=self.__prepare_general_headers())
        print("API_result:{0}".format(response.status_code))
        return response

    def __post_file_from_path(self, relative_url, path):
        print("API_requestor:{0}".format(relative_url))
        files = {'file': open(path, "rb")}
        print(API_ROOT_URL+relative_url)
        response = requests.post(API_ROOT_URL + relative_url, files=files, cookies=self.__prepare_auth_cookies(),
                                 headers=self.__prepare_general_headers())
        print("API_result:{0}".format(response.status_code))
        print(response.text)
        return response

    def __post(self, relative_url, body):
        print("API_requestor:{0}".format(relative_url))
        response = requests.post(API_ROOT_URL + relative_url, data=body, headers=self.__prepare_headers(),
                                 cookies=self.__prepare_auth_cookies())
        print("API_result:{0}".format(response.status_code))
        return response

    def __patch(self, relative_url, body):
        print("API_requestor:{0}".format(relative_url))
        response = requests.patch(API_ROOT_URL + relative_url, data=body, headers=self.__prepare_headers(),
                                  cookies=self.__prepare_auth_cookies())
        print("API_result:{0}".format(response.status_code))
        return response

    ###     INDIVIDUALS     ###
    def get_individual_info(self, id):
        path = URL_MAIN_INDIVIDUAL + f'{id}'
        return self.__get(path)

    def get_individual_cur_data_source(self, id):
        path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_MAIN_SUB_CUR_DATA + URL_MODULE_SOURCE
        return self.__get(path)

    def get_individual_cur_data_score(self, id):
        path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_MAIN_SUB_CUR_DATA + URL_MODULE_SCORING + URL_INDIVIDUAL_METHOD_SCORE
        return self.__get(path)[0]

    def get_individual_cur_data_parser_values(self, id):
        path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_MAIN_SUB_CUR_DATA + URL_MODULE_PARSER + URL_INDIVIDUAL_METHOD_VALUES
        return self.__get(path)

    def get_individual_cur_data_parser_validate_errors(self, id):
        path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_MAIN_SUB_CUR_DATA + URL_MODULE_PARSER + URL_INDIVIDUAL_METHOD_VALIDATE_ERRORS
        return self.__get(path)

    def get_individual_cur_data_parser_validate_status(self, id):
        path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_MAIN_SUB_CUR_DATA + URL_MODULE_PARSER + URL_INDIVIDUAL_METHOD_VALIDATE_STATUS
        return self.__get(path)

    def get_individual_cur_data_parser_stopfactor_status(self, id):
        path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_MAIN_SUB_CUR_DATA + URL_MODULE_PARSER + URL_INDIVIDUAL_METHOD_STOP_STATUS
        return self.__get(path)

    def get_individual_cur_data_parser_stopfactor_errors(self, id):
        path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_MAIN_SUB_CUR_DATA + URL_MODULE_PARSER + URL_INDIVIDUAL_METHOD_STOP_ERRORS
        return self.__get(path)

    def do_individual_accept(self, id):
        path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_INDIVIDUAL_OPS_POST_ACCEPT
        return self.__get(path)

    def do_individual_reject(self, id):
        path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_INDIVIDUAL_OPS_POST_REJECT
        return self.__get(path)

    def do_individual_pre_reject(self, id):
        path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_INDIVIDUAL_OPS_PRE_REJECT
        return self.__get(path)

    def do_individual_start(self, id):
        path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_INDIVIDUAL_OPS_START
        return self.__get(path)

    def do_individual_next(self, id):
        path = URL_MAIN_INDIVIDUAL + f'{id}' + URL_INDIVIDUAL_OPS_GEN_NEXT
        return self.__get(path)

    ###     MODULES     ###
    def get_module_view(self, module_name):
        path = URL_MAIN_MODULE + f'{module_name}/' + URL_MODULE_METHOD_VIEW
        return self.__get(path)

    def get_scoring_view(self):
        path = URL_MAIN_MODULE + URL_MODULE_SCORING + URL_MODULE_METHOD_VIEW
        return self.__get(path)

    def do_module_upload(self, module_name, request):
        path = URL_MAIN_MODULE + f'{module_name}' + URL_MODULE_METHOD_UPLOAD
        return self.__post_file(path, request)

    def do_module_upload_from_file(self, module_name, file_path):
        path = URL_MAIN_MODULE + f'{module_name}' + URL_MODULE_METHOD_UPLOAD
        print(path)
        print(file_path)
        return self.__post_file_from_path(path, file_path)

    def get_module_parser_parameters(self):
        path = URL_MAIN_MODULE + URL_MODULE_PARSER + URL_MODULE_METHOD_VIEW_PARAMETERS
        return self.__get(path)

    def get_module_parser_view(self):
        path = URL_MAIN_MODULE + URL_MODULE_PARSER + URL_MODULE_METHOD_VIEW
        return self.__get(path)

    def get_parser_module_by_name(self, name):
        return self.__get('/module/parser/{0}/'.format(name))[0]

    def get_scoring_module_by_name(self, name):
        return self.__get('/module/scoring/{0}/'.format(name))

    def get_report_basic(self):
        return self.__get('/report/general')

    def get_report_advanced(self):
        return self.__get('/report/advanced')

    ###     CLIENTS     ###
    def get_client_view(self, id):
        path = URL_MAIN_CLIENT + f'{id}' + URL_CLIENT_METHOD_VIEW
        return self.__get(path)

    def get_client_all(self):
        path = URL_MAIN_CLIENT
        return self.__get(path)

    def get_client_all_status(self):
        path = URL_MAIN_CLIENT + URL_CLIENT_METHOD_STATUS
        return self.__get(path)

    def get_client_by_status(self, status):
        path = URL_MAIN_CLIENT + status + '/'
        return self.__get(path)

    ###     PRODUCTS     ###
    def post_product(self, data):
        path = URL_MAIN_PRODUCT
        return self.__post(path, data)

    def patch_product(self, id, data):
        path = URL_MAIN_PRODUCT + f'{id}/'
        return self.__patch(path, data)

    def get_product(self, id):
        path = URL_MAIN_PRODUCT + f'{id}'
        return self.__get(path)

    def get_product_info(self):
        path = URL_MAIN_PRODUCT + URL_PRODUCT_METHOD_VIEW
        return self.__get(path)

    ###     USERS     ###
    def get_users(self):
        path = "/"+NAME_USER+"/"
        return self.__get(path)

    ### MESSAGE ####
    def send_message(self, message):
        path = "/"+NAME_MESSAGE+"/"
        return self.__post(path, message)

    ### ACTIONS ###
    def add_action(self, individual_id, action_type, processor, payload='None'):
        action = {}
        if processor == "user":
            try:
                session = Session.objects.get(session_key=self.__session)
                session_data = session.get_decoded()
                uid = session_data.get('_auth_user_id')
                user = User.objects.get(id=uid)
                action['processor'] = str(user)
            except Exception as e:
                print(traceback.format_exc())
                action['payload'] = traceback.format_exc()
                action['processor'] = processor
        else:
            action['processor'] = processor
        action['action_type'] = action_type
        action['payload'] = payload
        dumped_data = json.dumps(action, ensure_ascii=False)
        return self.__post('/individual/{0}/cur_gen/add_action/'.format(individual_id), dumped_data);

    ### CLIENT PROCESSOR ###
    def get_raw_willz(self, raw_willz_id):
        return self.__get(URL_MAIN_WILLZ + f'{raw_willz_id}/')

    def get_client_from_raw_willz(self, json_data):
        response = self.__post_decode(URL_MAIN_CLIENT, json_data)
        return response

    def update_client_product(self, client_id, json_data):
        path = URL_MAIN_CLIENT + f'{client_id}/' + URL_CLIENT_UPDATE_PRODUCT
        return self.__post(path, json_data)

    ### PARSER PROCESSOR ###

    def get_parser_body(self, parser):
        return self.__get(URL_MAIN_MODULE + URL_MODULE_PARSER + f'{parser}/')[0]

    def get_source_raw_data(self, individual_id, source_module_name):
        return self.__get(URL_MAIN_INDIVIDUAL + f'{individual_id}' +
                          URL_MAIN_SUB_CUR_DATA + URL_MODULE_SOURCE + f'{source_module_name}')

    def get_individual_json(self, individual_id):
        return self.__get(URL_MAIN_INDIVIDUAL + f'{individual_id}')

    def update_parser(self, individual_id, parser_m_name, parser_raw_data):
        return self.__post(
            URL_MAIN_INDIVIDUAL + f'{individual_id}' + URL_MAIN_SUB_CUR_DATA + URL_MODULE_PARSER + f'{parser_m_name}/',
            parser_raw_data)

    ### SCORING PROCESSOR ###

    def get_parser_method_values(self, individual_id):
        raw_data = self.__get(URL_MAIN_INDIVIDUAL + f'{individual_id}' + URL_MAIN_SUB_CUR_DATA
                              + URL_MODULE_PARSER + URL_INDIVIDUAL_METHOD_VALUES)
        return raw_data

    def update_scoring(self, individual_id, module_name, raw_data):
        return self.__post(
            URL_MAIN_INDIVIDUAL + f'{individual_id}' + URL_MAIN_SUB_CUR_DATA
            + URL_MODULE_SCORING + f'{module_name}/', raw_data)

    ### SOURCES PROCESSOR ###
    def get_source(self, source_name):
        return self.__get(URL_MAIN_MODULE + URL_MODULE_SOURCE + f'{source_name}/')[0]

    def update_source(self, individual_id, module_name, raw_data):
        return self.__post(
            URL_MAIN_INDIVIDUAL + f'{individual_id}' + URL_MAIN_SUB_CUR_DATA
            + URL_MODULE_SOURCE + f'{module_name}/',
            raw_data)

    ### WILLZ EXCEL CONVERTER ###
    def post_new_client(self, client_json):
        return self.__post(URL_MAIN_WILLZ+NAME_NEW+'/', client_json)

