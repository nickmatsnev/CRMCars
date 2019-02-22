#!/usr/bin/env python3
import json
import sys
import ast

from django.utils.baseconv import base64

from lib.modules import ParserModule

sys.path.append('../')

from lib import constants, api_requestor
from lib.process import *
from lib.json_encoders import DatetimeEncoder


class ParserProcessor(BasicProcess):


    def __init__(self):
        super(ParserProcessor, self).__init__(constants.PARSERS_PROCESSOR_QUEUE,
                                              {
                                                  constants.INDIVIDUAL_PARSERS_PROCESS_MESSAGE: self.__process_checks,
                                              })

    def __process_checks(self, body):
        input_message = json.loads(body)
        individual_id = input_message['individual_id']
        individual_json = api_requestor.request('/individual/{0}'.format(individual_id))
        parsers = input_message['parsers']
        raw_data = api_requestor.request('/individual/{0}/module_data/{1}/'.format(individual_id, "source"))['raw_data']

        sources_data = ast.literal_eval(raw_data)

        params_data = {}
        validations_data = {}

        for parser_dep in parsers:
            parser = api_requestor.request('/module/parser/{0}/'.format(parser_dep))[0]
            parser_m = ParserModule(parser['path'])
            src = parser_m.get_module_source()
            validate = parser_m.validate(individual_json, sources_data[src])

            validations_data[parser['name']] = validate

            params = parser_m.get_values(sources_data[src])
            new_dict = {item['name']: item['value'] for item in params}
            params_data[parser['name']] = new_dict

            api_requestor.post('/individual/{0}/module_data/{1}/'.format(individual_id, "parser_validate"),
                               json.dumps(({"raw_data": validations_data})))

            api_requestor.post('/individual/{0}/module_data/{1}/'.format(individual_id, "parser_parameters"),
                               json.dumps(({"raw_data": params_data}), cls=DatetimeEncoder))

            self._publish_message(constants.INDIVIDUAL_PARSERS_PROCESSED_MESSAGE,
                                  json.dumps({"individual_id": individual_id}))


proc = ParserProcessor()

proc.start()