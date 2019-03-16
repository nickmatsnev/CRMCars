#!/usr/bin/env python3
import ast
import sys
import json
from collections import ChainMap

from django.http.response import HttpResponse

sys.path.append('../')

sys.path.append('../../')

from lib import api_requestor, scoring_deps_helper, action_helper
import pandas

from lib.process import *
from lib.constants import *
from lib.modules import *




class ScoringProcessor(BasicProcess):
    products_cache = {1: 2}
    def __init__(self):
        super(ScoringProcessor, self).__init__(constants.SCORING_PROCESSOR_QUEUE,
                                               {
                                                   constants.INDIVIDUAL_SCORING_PROCESS: self.__process_scoring,
                                                   constants.INDIVIDUAL_SOURCE_PROCESSED_MESSAGE: self.__process_parsers,
                                                   constants.INDIVIDUAL_PARSER_PROCESSED_MESSAGE: self.__finalize_scoring
                                               })

    def __process_scoring(self, body):
        individual_data, individual_id = self.get_individual_data_for_message(body)
        source_deps = scoring_deps_helper.get_sources_deps(individual_data['scoring_module_id'])
        body_sources = {"individual_id": individual_id, "source": source_deps[0]}

        action_helper.add_action(individual_id, "scoring", "scoring_processor",
                                 payload="Начат процесс скоринга")
        self._publish_message(constants.INDIVIDUAL_SOURCE_PROCESS_MESSAGE, json.dumps(body_sources))

    def __process_parsers(self, body):
        individual_data, individual_id = self.get_individual_data_for_message(body)
        parsers_deps = scoring_deps_helper.get_parser_deps(individual_data['scoring_module_id'])

        body_parsers = {"individual_id": individual_id, "parser": parsers_deps[0]}

        action_helper.add_action(individual_id, "scoring", "parsers_processor")
        self._publish_message(constants.INDIVIDUAL_PARSER_PROCESS_MESSAGE, json.dumps(body_parsers))

    def __finalize_scoring(self, body):
        individual_data, individual_id = self.get_individual_data_for_message(body)

        action_helper.add_action(individual_id, "scoring_complete", "scoring_processor",
                                            payload="Завершен процесс скоринга")

        score_res = scoring_deps_helper.get_scoring_module(individual_data['scoring_module_id'])

        raw_data = api_requestor.request('/individual/{0}/cur_gen/data/parser/values/'.format(individual_id))

        parsers_parameters = ast.literal_eval(raw_data)

        res = score_res.get_score(parsers_parameters)

        api_requestor.post('/individual/{0}/cur_gen/data/{1}/'.format(individual_id, "scoring"),
                           json.dumps(({"score": res})))

        print("scoring")

    def get_individual_data_for_message(self, body):
        input_message = json.loads(body)
        individual_id = input_message['individual_id']
        individual_data = api_requestor.request('/individual/{0}'.format(individual_id))
        return individual_data, individual_id

proc = ScoringProcessor()
proc.start()
