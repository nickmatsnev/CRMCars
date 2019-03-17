#!/usr/bin/env python3
import ast
import json
import sys

from django.utils.baseconv import base64

sys.path.append('../')

sys.path.append('../../')
from lib import constants, api_requestor, action_helper
from lib.process import *
from lib.modules import SourceModule


class SourcesProcessor(BasicProcess):

        def __init__(self):
            super(SourcesProcessor, self).__init__(constants.SOURCES_PROCESSOR_QUEUE,
                                                   {
                                                       constants.INDIVIDUAL_SOURCE_PROCESS_MESSAGE: self.__process_sources
                                 })

        def __process_sources(self, body):
            input_message = json.loads(body)
            individual_id = input_message['individual_id']
            source_name = input_message['source']

            source = api_requestor.request('/module/source/{0}/'.format(source_name))[0]
            source_m = SourceModule(source['path'])
            credential = '{"username":"dmitry@korishchenko.ru","token":"4def557c4fa35791f07cc8d4faf7c3a5f7ae7c93"}'
                # TODO fix credentials
            data = source_m.import_data(credential, None)  # got scoring data

            raw_data = ast.literal_eval(json.dumps(data))
            api_requestor.post(
                '/individual/{0}/cur_gen/data/{1}/{2}/'.format(individual_id, "source", source_m.get_module_name()),
                raw_data)

            action_helper.add_action(individual_id, "scoring", "sources_processor",
                                                payload="Загружен источник: {0}".format(source_m.get_module_name()))

            self._publish_message(constants.INDIVIDUAL_SOURCE_PROCESSED_MESSAGE,
                                  json.dumps({"individual_id": individual_id}))


proc = SourcesProcessor()
proc.start()