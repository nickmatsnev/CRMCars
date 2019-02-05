#!/usr/bin/env python3
import sys
sys.path.append('../')


from lib import constants
from lib.process import *



class ChecksProcessor(BasicProcess):


    def __init__(self):
        super(ChecksProcessor, self).__init__( constants.CHECKS_PROCESSOR_QUEUE,
                              {
                                constants.INDIVIDUAL_CHECKS_PROCESS_MESSAGE: self.__process_checks,
                             })

    def __process_checks(self, body):
        print("checks are processed")
        ChecksProcessor.get_processor_name()
        self._publish_message(constants.INDIVIDUAL_CHECKS_PROCESSED_MESSAGE,"test_body")


proc = ChecksProcessor()

proc.start()