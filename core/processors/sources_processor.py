#!/usr/bin/env python3
import ast
import json
import sys
import traceback

from lib.constants import *
from lib import parser_values_converter

sys.path.append('../')

sys.path.append('../../')

from lib.process import *
from lib.modules import SourceModule, SOURCE_PROCESSOR_USERNAME
from lib.api import *


class SourcesProcessor(BasicProcess):

        def __init__(self):
            super(SourcesProcessor, self).__init__(constants.SOURCES_PROCESSOR_QUEUE,
                                                   {
                                                       constants.INDIVIDUAL_SOURCE_PROCESS_MESSAGE: self.__process_sources
                                 })

        def get_name(self):
            return SOURCE_PROCESSOR_NAME

        def __process_sources(self, body):
            input_message = json.loads(body)
            individual_id = input_message['individual_id']
            source_name = input_message['source']
            no_module_name = True

            try:
                source = self._apiRequestor.get_source(source_name)
                source_m = SourceModule(source['path'])
                no_module_name = False

                base_credential = {"username":SOURCE_PROCESSOR_USERNAME,"token":SOURCE_PROCESSOR_TOKEN}
                credential = json.dumps(base_credential)

                individual_json = self._apiRequestor.get_individual_json(individual_id)
                parsers_data = self._apiRequestor.get_parser_method_values(individual_id)

                parsers_parameters = parser_values_converter.get_parser_values(parsers_data)
                data = source_m.import_data(credential, individual_json, parsers_parameters)  # got scoring data

                # raw_data = ast.literal_eval(json.dumps(data))
                raw_data = json.dumps(data)
                self._apiRequestor.update_source(individual_id, source_m.get_module_name(), raw_data)

                self._apiRequestor.add_action(individual_id, NAME_SCORING, NAME_SOURCES_PROCESSOR,
                                                payload=SOURCE_PROCESSOR_SOURCE_LOADED + f'{source_m.get_module_name()}')

                self._publish_message(constants.INDIVIDUAL_SOURCE_PROCESSED_MESSAGE,
                                      json.dumps({"individual_id": individual_id, "parser": input_message['parser']}))

            except Exception as e:
                if no_module_name==True:
                    payload = SOURCE_PROCESSOR_ERR_MODULE_NAME + traceback.format_exc()
                else:
                    payload = SOURCE_PROCESSOR_ERR_STRUCTURE + traceback.format_exc()

                self._publish_message(constants.INDIVIDUAL_SOURCE_ERROR_MESSAGE,
                                      json.dumps({"individual_id": individual_id,"payload": payload}))


proc = SourcesProcessor()
proc.start()