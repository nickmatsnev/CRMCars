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
        input_message = json.loads(body)
        client_id = input_message['raw_client_id']
        factory = APIRequestFactory()
        request = factory.get('/api/willz/{0}'.format(client_id))
        RawData = json.loads(request)
        RawJson = RawData['payload']

        JsonToClient = json.dump({'willz_id': RawJson['id'],'created_at': RawJson['created_at']})
        request = factory.post('/api/clients',json.dumps(RawJson), content_type='application/json')
        RawRequest = json.loads(request)
        ClientID = RawRequest['id']

# я подумал и решил что мы будем выводить тупо первого физика, а проверку на первость можно провести тут, тогда не нужно будет доп поле и еще код
        for drvr in range(0, len(RawJson['drivers'])):
            json_driver = RawJson['drivers'][drvr]
            if json_driver['id'] == RawJson['driver_id']:
                factory.post('/api/clients/{0}/individuals'.format(ClientID), json.dumps(json_driver),
                             content_type='application/json')
                break

        for drvr in range(0, len(RawJson['drivers'])):
            json_driver = RawJson['drivers'][drvr]
            if json_driver['id'] != RawJson['driver_id']:
                factory.post('/api/clients/{0}/individuals'.format(ClientID), json.dumps(json_driver), content_type='application/json')

        print("client is processed")
        self._publish_message(CLIENT_PROCESSED_MESSAGE,"test_body")




proc = ClientProcessor()
proc.start()
