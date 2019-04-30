#!/usr/bin/env python3
import json
import sys

from lib.constants import *

sys.path.append('../')

sys.path.append('../../')

from lib import parser_helper

from lib import parser_values_converter

from lib.process import *



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
        source_deps = parser_helper.get_sources_deps(self._apiRequestor, individual_data['scoring_module_id'])
        body_sources = {"individual_id": individual_id, "source": source_deps[0]['source'],
                        "parser": source_deps[0]['parser']}

        self._apiRequestor.add_action(individual_id, NAME_SCORING, NAME_SCORING_PROCESSOR,
                                      payload=SCORING_PROCESSOR_SCORING_START)
        self._publish_message(constants.INDIVIDUAL_SOURCE_PROCESS_MESSAGE, json.dumps(body_sources))

    def __process_parsers(self, body):
        individual_data, individual_id, parser_name = self.get_individual_data_for_message_with_parser(body)

        body_parsers = {"individual_id": individual_id, "parser": parser_name}

        self._apiRequestor.add_action(individual_id, NAME_SCORING, NAME_PARSERS_PROCESSOR,
                                      payload=SCORING_PROCESSOR_PARSING_START)
        self._publish_message(constants.INDIVIDUAL_PARSER_PROCESS_MESSAGE, json.dumps(body_parsers))

    def __finalize_scoring(self, body):
        individual_data, individual_id = self.get_individual_data_for_message(body)

        source_deps = parser_helper.get_sources_deps(self._apiRequestor, individual_data['scoring_module_id'])
        finished_sources = self._apiRequestor.get_individual_cur_data_source(individual_id)
        fin = list(finished_sources.keys())
        all_sources = list(map(lambda x: x['source'], source_deps))
        for source in fin:
            all_sources.remove(source)
        if all_sources:
            next_source = all_sources[0]
            next_parser = None
            for source_dep in source_deps:
                if source_dep['source'] == next_source:
                    next_parser = source_dep['parser']
                    break;

            body_sources = {"individual_id": individual_id, "source": next_source,
                            "parser": next_parser}
            self._publish_message(constants.INDIVIDUAL_SOURCE_PROCESS_MESSAGE, json.dumps(body_sources))
            print("next source...")
            return

        raw_data = self._apiRequestor.get_parser_method_values(individual_id)

        parsers_parameters = parser_values_converter.get_parser_values(raw_data)

        score_res = parser_helper.get_scoring_module(self._apiRequestor, individual_data['scoring_module_id'])
        res = score_res.get_score(parsers_parameters)

        self._apiRequestor.update_scoring(individual_id, score_res.get_module_name(), json.dumps({"Score": res}))

        self._apiRequestor.add_action(individual_id, NAME_SCORING_COMPLETE, NAME_SCORING_PROCESSOR,
                                 payload=SCORING_PROCESSOR_SCORING_STOP)

        print("scoring done...")

    def get_individual_data_for_message(self, body):
        input_message = json.loads(body)
        individual_id = input_message['individual_id']
        individual_data = self._apiRequestor.get_individual_json(individual_id)
        return individual_data, individual_id

    def get_individual_data_for_message_with_parser(self, body):
        input_message = json.loads(body)
        individual_id = input_message['individual_id']
        individual_data = self._apiRequestor.get_individual_json(individual_id)
        parser_name = input_message['parser']
        return individual_data, individual_id, parser_name


    def __error_source(self, body):
        input_message = json.loads(body)
        individual_id = input_message['individual_id']
        payload = input_message['payload']
        self._apiRequestor.add_action(individual_id, NAME_SCORING_CHECKS_FAILED, NAME_SOURCES_PROCESSOR,
                                      payload=payload)


    def __error_parser(self, body):
        input_message = json.loads(body)
        individual_id = input_message['individual_id']
        payload = input_message['payload']
        self._apiRequestor.add_action(individual_id, NAME_SCORING_CHECKS_FAILED, NAME_PARSERS_PROCESSOR,
                                      payload=payload)

proc = ScoringProcessor()
proc.start()
