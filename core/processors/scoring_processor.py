#!/usr/bin/env python3
import sys
import json

sys.path.append('../')

sys.path.append('../../')

from lib import basic_api_requestor, scoring_deps_helper, action_helper

from lib.scoring_value_converter import convert

from lib.process import *
from lib.constants import *




class ScoringProcessor(BasicProcess):
    products_cache = {1: 2}
    def __init__(self):
        super(ScoringProcessor, self).__init__(constants.SCORING_PROCESSOR_QUEUE,
                                               {
                                                   constants.INDIVIDUAL_SCORING_PROCESS: self.__process_scoring,
                                                   constants.INDIVIDUAL_SOURCE_PROCESSED_MESSAGE: self.__process_parsers,
                                                   constants.INDIVIDUAL_PARSER_PROCESSED_MESSAGE: self.__finalize_scoring,
                                                   constants.INDIVIDUAL_SOURCE_ERROR_MESSAGE: self.__error_source,
                                                   constants.INDIVIDUAL_PARSER_ERROR_MESSAGE: self.__error_parser,
                                               })

    def __process_scoring(self, body):
        individual_data, individual_id = self.get_individual_data_for_message(body)
        source_deps = scoring_deps_helper.get_sources_deps(individual_data['scoring_module_id'])
        body_sources = {"individual_id": individual_id, "source": source_deps[0]}

        action_helper.add_action(individual_id, "scoring", "scoring_processor",
                                 payload=SCORING_PROCESSOR_SCORING_START)
        self._publish_message(constants.INDIVIDUAL_SOURCE_PROCESS_MESSAGE, json.dumps(body_sources))

    def __process_parsers(self, body):
        individual_data, individual_id = self.get_individual_data_for_message(body)
        parsers_deps = scoring_deps_helper.get_parser_deps(individual_data['scoring_module_id'])

        body_parsers = {"individual_id": individual_id, "parser": parsers_deps[0]}

        action_helper.add_action(individual_id, "scoring", "parsers_processor",
                                 payload=SCORING_PROCESSOR_PARSING_START)
        self._publish_message(constants.INDIVIDUAL_PARSER_PROCESS_MESSAGE, json.dumps(body_parsers))

    def __finalize_scoring(self, body):
        individual_data, individual_id = self.get_individual_data_for_message(body)


        score_res = scoring_deps_helper.get_scoring_module(individual_data['scoring_module_id'])

        raw_data = basic_api_requestor.request(URL_MAIN_INDIVIDUAL + f'/{individual_id}'+ URL_MAIN_SUB_CUR_DATA + '/'
                                               +URL_MODULE_PARSER+URL_INDIVIDUAL_METHOD_VALUES)

        parsers_parameters = convert(raw_data)

        res = score_res.get_score(parsers_parameters)

        basic_api_requestor.post(
            URL_MAIN_INDIVIDUAL + f'/{individual_id}' + URL_MAIN_SUB_CUR_DATA + '/'
            + URL_MODULE_SCORING + f'{score_res.get_module_name()}' + "/",
            json.dumps(({"Score": res})))
        action_helper.add_action(individual_id, "scoring_complete", "scoring_processor",
                                 payload=SCORING_PROCESSOR_SCORING_STOP)

        print("scoring")

    def get_individual_data_for_message(self, body):
        input_message = json.loads(body)
        individual_id = input_message['individual_id']
        individual_data = basic_api_requestor.request(URL_MAIN_INDIVIDUAL + '/{0}'.format(individual_id))
        return individual_data, individual_id


    def __error_source(self, body):
        input_message = json.loads(body)
        individual_id = input_message['individual_id']
        payload = input_message['payload']
        action_helper.add_action(individual_id, "scoring_checks_failed", "sources_processor",
                                 payload=payload)


    def __error_parser(self, body):
        input_message = json.loads(body)
        individual_id = input_message['individual_id']
        payload = input_message['payload']
        action_helper.add_action(individual_id, "scoring_checks_failed", "parsers_processor",
                                 payload=payload)

proc = ScoringProcessor()
proc.start()
