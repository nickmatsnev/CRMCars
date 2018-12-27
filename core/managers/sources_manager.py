#!/usr/bin/env python3
import sys
#simport redis
sys.path.append('../')


from lib import constants
from lib.process import *




class SourcesManager(BasicProcess):

    def __init__(self):
        super(SourcesManager, self).__init__(constants.SOURCES_MANAGER_QUEUE,
                              {
                                  constants.INDIVIDUAL_SOURCES_PROCESS_MESSAGE: self.__process_all_sources,
                                  constants.SCORISTA_SOURCE_PROCESSED_MESSAGE: self.__scorista_source_processed,

                              })
        #__redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    def __process_all_sources(self, body):
        print("client start sources process")
        #__redis.set("555","{scorista:undone}")

        self._publish_message(constants.SCORISTA_SOURCE_PROCESS_MESSAGE, "test_body")

    def __scorista_source_processed(self, body):
        print("scorista source processed")
        #__redis.get("555")
        self.__send_complete_sources()

    def __send_complete_sources(self):
        print("all sources processed")
        self._publish_message(constants.INDIVIDUAL_SOURCES_PROCESSED_MESSAGE,"test_body")

proc = SourcesManager()
proc.start()
