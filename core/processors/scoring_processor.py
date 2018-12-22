#!/usr/bin/env python3
import sys
sys.path.append('../')



from lib.process import *
from lib.constants import *


class ScoringProcessor(BasicProcess):

    def __init__(self):
        super(ScoringProcessor, self).__init__(constants.SCORING_PROCESSOR_QUEUE,
                             {
                                 constants.INDIVIDUAL_SCORING_PROCESS: self.__process_scoring
                             })

    def __process_scoring(self, body):
        print("scoring is processed")
        self._publish_message(constants.INDIVIDUAL_SCORING_PROCESSED_MESSAGE, "test_body")

proc = ScoringProcessor()
proc.start()