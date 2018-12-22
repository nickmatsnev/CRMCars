#!/usr/bin/env python3
import sys
sys.path.append('../')


from lib import constants
from lib.process import *

class ScoringManager(BasicProcess):

    def __init__(self):
        super(ScoringManager, self).__init__(constants.SCORING_MANAGER_QUEUE,
                              {
                                  constants.CLIENT_PROCESSED_MESSAGE: self.__client_processed,
                                  constants.INDIVIDUAL_SOURCES_PROCESSED_MESSAGE: self.__client_sources_processed,
                                  constants.INDIVIDUAL_CHECKS_PROCESSED_MESSAGE:self.__client_checks_processed,
                                  constants.INDIVIDUAL_SCORING_PROCESSED_MESSAGE:self.__client_scoring_processed
                              })

    def __client_processed(self, body):
        print("client is processed")
        self._publish_message(constants.INDIVIDUAL_SOURCES_PROCESS_MESSAGE, "test_body")

    def __client_sources_processed(self, body):
        print("client sources are processed")
        self._publish_message(constants.INDIVIDUAL_CHECKS_PROCESS_MESSAGE,"test_body")

    def __client_checks_processed(self,body):
        print("client checks are processed")
        self._publish_message(constants.INDIVIDUAL_SCORING_PROCESS,"test_body")

    def __client_scoring_processed(self,body):
        print("client scoring is processed")
        self._publish_message(constants.CLIENT_SCORING_COMPLETE_MESSAGE,"test_body")



proc = ScoringManager()
proc.start()
