#!/usr/bin/env python3
import sys
sys.path.append('../')


from lib.process import *
from lib.constants import *
from rest_framework.test import APIRequestFactory

import json

class ClientProcessor(BasicProcess):

    def __init__(self):
        super(ClientProcessor,self).__init__(constants.CLIENT_PROCESSOR_QUEUE,
                              {
                                constants.CLIENT_RAW_CREATED_MESSAGE:self.__process_raw_client
                             })

    def __process_raw_client(self, body):
        factory = APIRequestFactory()
        request = factory.post('/api/willz/{0}'.format(7))

        #raw_client_id = json.parse ....
        #api call get_raw_client_data
        # parse raw_client_data
        #api_call insert image.. license .. passport ...
        # r = requests.post("localhost:8000/api/create_passport","data:pass")
        #test_body = json = individual_id = 555 ....
        print("client is processed")
        self._publish_message(CLIENT_PROCESSED_MESSAGE,"test_body")




proc = ClientProcessor()
proc.start()
