#!/usr/bin/env python3
import sys
import json
import requests

sys.path.append('../')

from lib.global_settings import API_ROOT_URL
from lib import basic_api_requestor, action_helper, willz_to_client
from lib.process import *
from lib.constants import *


class ClientProcessor(BasicProcess):

    def __init__(self):
        super(ClientProcessor, self).__init__(constants.CLIENT_PROCESSOR_QUEUE,
                                              {
                                                  constants.CLIENT_RAW_CREATED_MESSAGE: self.__process_raw_client
                                              })

    def get_name(self):
        return CLIENT_PROCESSOR_NAME

    def __process_raw_client(self, body):

            # дергаем сырок
            input_message = json.loads(body)
            raw_client_id = input_message['raw_client_id']
            raw_data = basic_api_requestor.request(URL_MAIN_WILLZ+'/{0}/'.format(raw_client_id))
            # парсим payload виллзовский
            raw_json = json.loads(raw_data['payload'])

            new_client = willz_to_client.convert(raw_json)
            json_data = json.dumps(new_client)

            try:
                response = requests.post(API_ROOT_URL + URL_MAIN_CLIENT + '/', data=json_data,
                                         headers = {'Content-Type': 'application/json'})
                client = json.loads(response.content.decode('utf-8'))

                client_id = client['id']

                json_data = json.dumps({"product":"Willz"})
                response = requests.post(API_ROOT_URL + URL_MAIN_CLIENT+f'/{client_id}/'
                                         + URL_CLIENT_UPDATE_PRODUCT, data=json_data,
                                         headers={'Content-Type': 'application/json'})

                for individual in client['individuals']:
                    action_helper.add_action(individual['id'], 'new', self.get_name(),
                                             payload=CLIENT_PROCESSOR_WILLZ_SUCCESS)


                print(CLIENT_PROCESSOR_SUCCESS)

            except:
                print(CLIENT_PROCESSOR_NOT_SUCCESS)


proc = ClientProcessor()
proc.start()
