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
        input_message = json.loads(body)
        product_id = input_message['product_id']
        individual_id = input_message['individual_id']
        self.products_cache[individual_id] = product_id;

        source_deps = scoring_deps_helper.get_sources_deps(product_id)
        body_sources = {"individual_id": individual_id, "source": source_deps[0]}

        action_helper.add_action_individual(individual_id, "scoring", "scoring_processor",
                                            payload="Начат процесс скоринга")
        self._publish_message(constants.INDIVIDUAL_SOURCE_PROCESS_MESSAGE, json.dumps(body_sources))

    def __process_parsers(self, body):
        input_message = json.loads(body)
        individual_id = input_message['individual_id']
        parsers_deps = scoring_deps_helper.get_parser_deps(self.products_cache[individual_id])
        body_parsers = {"individual_id": individual_id, "parser": parsers_deps[0]}

        action_helper.add_action_individual(individual_id, "scoring", "parsers_processor")
        self._publish_message(constants.INDIVIDUAL_PARSER_PROCESS_MESSAGE, json.dumps(body_parsers))

    def __finalize_scoring(self, body):
        input_message = json.loads(body)
        individual_id = input_message['individual_id']
        action_helper.add_action_individual(individual_id, "scoring_complete", "scoring_processor",
                                            payload="Завершен процесс скоринга")
        score_res = scoring_deps_helper.get_scoring_module(self.products_cache[individual_id])

        raw_data = api_requestor.request('/individual/{0}/data/parser/values/'.format(individual_id))

        parsers_parameters = ast.literal_eval(raw_data)

        res = score_res.get_score(parsers_parameters)

        api_requestor.post('/individual/{0}/module_data/{1}/'.format(individual_id, "scoring"),
                           json.dumps(({"score": res})))

        print("scoring")


proc = ScoringProcessor()
proc.start()
