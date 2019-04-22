#!/usr/bin/env python3
import json
import sys


sys.path.append('../')
sys.path.append('../../')

from lib.constants import *

from lib import willz_to_client
from lib.process import *


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

            raw_data = self._apiRequestor.get_raw_willz(raw_client_id)
            # парсим payload виллзовский
            raw_json = json.loads(raw_data['payload'])

            new_client = willz_to_client.convert(raw_json)
            json_data = json.dumps(new_client)

            try:
                client = self._apiRequestor.get_client_from_raw_willz(json_data)

                client_id = client['id']

                json_data = json.dumps({"product":"Willz"})
                response = self._apiRequestor.update_client_product(client_id, json_data)

                for individual in client['individuals']:
                    self._apiRequestor.add_action(individual['id'], NAME_NEW, self.get_name(),
                                                  payload=CLIENT_PROCESSOR_WILLZ_SUCCESS)


                print(CLIENT_PROCESSOR_SUCCESS)

            except:
                print(CLIENT_PROCESSOR_NOT_SUCCESS)


proc = ClientProcessor()
proc.start()
