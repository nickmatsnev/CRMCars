#!/usr/bin/env python3
import ast
import sys

sys.path.append('../')

sys.path.append('../../')
from lib import action_helper
from lib.process import *
from lib.modules import SourceModule
from lib.api_requestor import *


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
                source = get_source(source_name)
                source_m = SourceModule(source['path'])
                no_module_name = False

                base_credential = {"username":SOURCE_PROCESSOR_USERNAME,"token":SOURCE_PROCESSOR_TOKEN}
                credential = json.dumps(base_credential)

                individual_json = get_individual_json(individual_id)
                data = source_m.import_data(credential, individual_json)  # got scoring data

                raw_data = ast.literal_eval(json.dumps(data))

                update_source(individual_id,source_m.get_module_name(),raw_data)

                action_helper.add_action(individual_id, NAME_SCORING, NAME_SOURCES_PROCESSOR,
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