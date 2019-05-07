#!/usr/bin/env python3
import json
import sys
import traceback



sys.path.append('../')
sys.path.append('../../')
from lib.constants import *

from lib.modules import ParserModule

from lib.process import *
from lib.json_encoders import DatetimeEncoder


class ParserProcessor(BasicProcess):

    def __init__(self):
        super(ParserProcessor, self).__init__(constants.PARSERS_PROCESSOR_QUEUE,
                                              {
                                                  constants.INDIVIDUAL_PARSER_PROCESS_MESSAGE: self.__process_checks,
                                              })

    def get_name(self):
        return constants.PARSER_PROCESSOR_NAME

    def __process_checks(self, body):
        input_message = json.loads(body)
        individual_id = input_message['individual_id']

        parser = input_message['parser']

        no_module_name = True
        no_validation = True
        no_stopfactors = True
        no_params = True

        try:
            parser = self._apiRequestor.get_parser_body(parser)
            parser_m = ParserModule(parser['path'])
            no_module_name = False

            parser_m_name = parser_m.get_module_name()
            source_module_name = parser_m.get_module_source()

            source_raw_data = self._apiRequestor.get_source_raw_data(individual_id, source_module_name)

            individual_json = self._apiRequestor.get_individual_json(individual_id)

            validate = parser_m.validate(individual_json, source_raw_data)
            no_validation = False
            stop_factors = parser_m.stop_factors(individual_json, source_raw_data)
            no_stopfactors = False
            params = parser_m.get_values(source_raw_data)
            no_params = False

            parser_object = {constants.NAME_VVALUES: params, constants.NAME_VVALIDATE: validate,
                             constants.NAME_SSTOPFFACTORS: stop_factors}
            parser_raw_data = json.dumps(parser_object, cls=DatetimeEncoder)

            self._apiRequestor.update_parser(individual_id, parser_m_name, parser_raw_data)

            self._apiRequestor.add_action(individual_id, NAME_SCORING, NAME_PARSERS_PROCESSOR,
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
                                  json.dumps(
                                      {"individual_id": individual_id, "payload": payload + traceback.format_exc()}))




proc = ParserProcessor()

proc.start()
