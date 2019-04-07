#!/usr/bin/env python3
import json
import sys

sys.path.append('../')

from lib.modules import ParserModule
from lib import basic_api_requestor, action_helper
from lib.process import *
from lib.json_encoders import DatetimeEncoder
from lib.constants import *


class ParserProcessor(BasicProcess):


    def __init__(self):
        super(ParserProcessor, self).__init__(constants.PARSERS_PROCESSOR_QUEUE,
                                              {
                                                  constants.INDIVIDUAL_PARSER_PROCESS_MESSAGE: self.__process_checks,
                                              })

    def __process_checks(self, body):
        input_message = json.loads(body)
        individual_id = input_message['individual_id']

        parser = input_message['parser']
        no_module_name = True
        no_validation = True
        no_stopfactors = True
        no_params = True

        try:
            parser = basic_api_requestor.request(URL_MAIN_MODULE + '/' + URL_MODULE_PARSER + f'{parser}/')[0]
            parser_m = ParserModule(parser['path'])
            no_module_name = False

            parser_m_name = parser_m.get_module_name()
            source_module_name = parser_m.get_module_source()

            source_raw_data = basic_api_requestor.request(
            URL_MAIN_INDIVIDUAL + f'/{individual_id}' + URL_MAIN_SUB_CUR_DATA + '/' +
            URL_MODULE_SOURCE +f'{source_module_name}')

            individual_json = basic_api_requestor.request(URL_MAIN_INDIVIDUAL+f'/{individual_id}')

            validate = parser_m.validate(individual_json, source_raw_data)
            no_validation = False
            stop_factors = parser_m.stop_factors(individual_json, source_raw_data)
            no_stopfactors = False
            params = parser_m.get_values(source_raw_data)
            no_params = False

            parser_object = {'Values': params, 'Validate': validate, 'StopFactors': stop_factors}
            parser_raw_data = json.dumps(parser_object, cls=DatetimeEncoder)

            basic_api_requestor.post(
            URL_MAIN_INDIVIDUAL+f'/{individual_id}'+URL_MAIN_SUB_CUR_DATA+'/'+URL_MODULE_PARSER+f'{parser_m_name}/',
            parser_raw_data)

            action_helper.add_action(individual_id, "scoring", "parsers_processor",
                                 payload=PARSER_PROCESSOR_SUCCESS + f'{parser_m_name}')

            self._publish_message(constants.INDIVIDUAL_PARSER_PROCESSED_MESSAGE,
                              json.dumps({"individual_id": individual_id}))

        except Exception as e:
            if no_module_name == True:
                payload = PARSER_PROCESSOR_ERR_MODULE_NAME
            elif no_validation == True:
                payload = PARSER_PROCESSOR_ERR_VALIDATION
            elif no_stopfactors == True:
                payload = PARSER_PROCESSOR_ERR_STOP_FACTORS
            elif no_params == True:
                payload = PARSER_PROCESSOR_ERR_PARAMS
            else:
                payload = PARSER_PROCESSOR_UNKNOWN

            self._publish_message(constants.INDIVIDUAL_PARSER_ERROR_MESSAGE,
                                    json.dumps({"individual_id": individual_id, "payload": payload+str(e)}))

proc = ParserProcessor()

proc.start()