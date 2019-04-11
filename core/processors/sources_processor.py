#!/usr/bin/env python3
import ast
import json
import sys

from lib.constants import *

sys.path.append('../')

sys.path.append('../../')

from lib.process import *
from lib.modules import SourceModule, SOURCE_PROCESSOR_USERNAME



class SourcesProcessor(BasicProcess):

        def __init__(self):
            super(SourcesProcessor, self).__init__(constants.SOURCES_PROCESSOR_QUEUE,
                                                   {
                                                       constants.INDIVIDUAL_SOURCE_PROCESS_MESSAGE: self.__process_sources
                                 })

        def __process_sources(self, body):
            input_message = json.loads(body)
            individual_id = input_message['individual_id']
            source_name = input_message['source']  # TODO fixxx to sources
            no_module_name = True

            try:
                source = self._apiRequestor.get_source(source_name)
                source_m = SourceModule(source['path'])
                no_module_name = False

                base_credential = {"username":SOURCE_PROCESSOR_USERNAME,"token":SOURCE_PROCESSOR_TOKEN}
                credential = json.dumps(base_credential)
                # TODO fix credentials
                data = source_m.import_data(credential, None)  # got scoring data

                raw_data = ast.literal_eval(json.dumps(data))

                self._apiRequestor.update_source(individual_id, source_m.get_module_name(), raw_data)

                self._apiRequestor.add_action(individual_id, NAME_SCORING, NAME_SOURCES_PROCESSOR,
                                                payload=SOURCE_PROCESSOR_SOURCE_LOADED + f'{source_m.get_module_name()}')

                self._publish_message(constants.INDIVIDUAL_SOURCE_PROCESSED_MESSAGE,
                                  json.dumps({"individual_id": individual_id}))

            except Exception as e:
                if no_module_name==True:
                    payload = SOURCE_PROCESSOR_ERR_MODULE_NAME + str(e)
                else:
                    payload = SOURCE_PROCESSOR_ERR_STRUCTURE + str(e)

                self._publish_message(constants.INDIVIDUAL_SOURCE_ERROR_MESSAGE,
                                      json.dumps({"individual_id": individual_id,"payload": payload}))


proc = SourcesProcessor()
proc.start()