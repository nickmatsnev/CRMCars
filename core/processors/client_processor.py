#!/usr/bin/env python3
import sys
import json
import requests

from django.http.response import HttpResponse

sys.path.append('../')

from lib.global_settings import API_ROOT_URL
from lib import api_requestor, action_helper, willz_to_client
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
            raw_data = api_requestor.request('/willz/{0}/'.format(raw_client_id))
            # парсим payload виллзовский
            raw_json = json.loads(raw_data['payload'])

            new_client = willz_to_client.convert(raw_json)
            json_data = json.dumps(new_client)

            try:
                response = requests.post(API_ROOT_URL + '/client/', data=json_data,
                                         headers = {'Content-Type': 'application/json'})
                client = json.loads(response.content.decode('utf-8'))

                client_id = client['id']

                json_data = json.dumps({"product":"Willz"})
                response = requests.post(API_ROOT_URL + '/client/{0}/update_product/'.format(client_id), data=json_data,
                                         headers={'Content-Type': 'application/json'})

                action = {}
                action['processor'] = self.get_name()
                action['action_type'] = 'new'

                json_data = json.dumps(action)
                response = requests.post(API_ROOT_URL +'/client/{0}/add_action/'.format(client_id), json_data,
                                              headers = {'Content-Type': 'application/json'})

                print(" client is processed")

            except:
                print(" client is not processed")


proc = ClientProcessor()
proc.start()
