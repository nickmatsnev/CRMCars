#!/usr/bin/env python3
import ast
import json
import sys

from django.utils.baseconv import base64

sys.path.append('../')

sys.path.append('../../')
from lib import constants, api_requestor
from lib.process import *
from lib.modules import SourceModule


class SourcesProcessor(BasicProcess):

        def __init__(self):
            super(SourcesProcessor, self).__init__(constants.SOURCES_PROCESSOR_QUEUE,
                                                   {
                                                       constants.INDIVIDUAL_SOURCES_PROCESS_MESSAGE: self.__process_sources
                                 })

        def __process_sources(self, body):
            input_message = json.loads(body)
            individual_id = input_message['individual_id']
            sources = input_message['sources']  # TODO fixxx to sources

            source_data = {}

            for source_dep in sources:
                source = api_requestor.request('/module/source/{0}/'.format(source_dep))[0]
                source_m = SourceModule(source['path'])
                data = source_m.import_data(source['credentials'], None)  # got scoring data
                source_data["{0}".format(source['name'])] = data
            raw_data = ast.literal_eval(json.dumps(source_data))
            api_requestor.post('/individual/{0}/module_data/{1}/'.format(individual_id, "source"),
                               json.dumps({"raw_data": raw_data}))

            self._publish_message(constants.INDIVIDUAL_SOURCES_PROCESSED_MESSAGE,
                                  json.dumps({"individual_id": individual_id}))


proc = SourcesProcessor()
proc.start()