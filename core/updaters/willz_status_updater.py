#!/usr/bin/env python3
import sys
sys.path.append('../')


from lib import constants
from lib.process import *


class WillzStatusUpdater(BasicProcess):

        def __init__(self):
            super(WillzStatusUpdater, self).__init__(constants.WILLZ_STATUS_UPDATER_QUEUE,
                                  {
                                     constants.CLIENT_SCORING_COMPLETE_MESSAGE: self.__willz_update_status
                                 })

        def __willz_update_status(self, body):
            print("willz status is updated")



proc = WillzStatusUpdater()
proc.start()