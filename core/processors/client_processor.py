#!/usr/bin/env python3
import sys
sys.path.append('../')



from lib.process import *
from lib.constants import *



class ClientProcessor(BasicProcess):

    def __init__(self):
        super(ClientProcessor,self).__init__(constants.CLIENT_PROCESSOR_QUEUE,
                              {
                                constants.CLIENT_RAW_CREATED_MESSAGE:self.__process_raw_client
                             })

    def __process_raw_client(self, body):
        print("client is processed")
        self._publish_message(CLIENT_PROCESSED_MESSAGE,"test_body")




proc = ClientProcessor()
proc.start()
