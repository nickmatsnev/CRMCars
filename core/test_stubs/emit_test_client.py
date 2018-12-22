#!/usr/bin/env python3
import sys
sys.path.append('../')


from lib import constants
import pika

from lib.process import *

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()
channel.basic_publish(constants.MAIN_EXCHANGE_NAME,
                      routing_key=constants.CLIENT_RAW_CREATED_MESSAGE,
                      body="test", properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
