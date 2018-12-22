#!/usr/bin/env python3
import sys
sys.path.append('../')


from lib import constants
from lib.process import *


class ScoristaProcessor(BasicProcess):

        def __init__(self):
            super(ScoristaProcessor, self).__init__(constants.SCORISTA_PROCESSOR_QUEUE,
                                  {
                                     constants.SCORISTA_SOURCE_PROCESS_MESSAGE: self.__process_source
                                 })

        def __process_source(self, body):
            print("source scorista is processed")
            self._publish_message(constants.SCORISTA_SOURCE_PROCESSED_MESSAGE, "test_body")


proc = ScoristaProcessor()
proc.start()