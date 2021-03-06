#!/usr/bin/env python3
import os
import sys
from datetime import datetime, time
import pika

from core.lib import constants
from core.lib.global_settings import BUS_HOST
from lib.api import ApiRequestor

from django.core.files import File

from contextlib import redirect_stdout

from lib.stdout_redirector import StdoutRedirector


class BasicProcess:
    __host = BUS_HOST
    _apiRequestor = ApiRequestor()

    def __init__(self,queue_name="",callbacks=None
                 ):
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.__host))
        self.__channel = self.__connection.channel()
        #consume not more than one message at time (between rcv & ack)
        self.__channel.basic_qos(prefetch_count=1)

        try:
            self.__channel.basic_consume(queue_name, self.callback)
        except:
            self.__channel.basic_consume(self.callback, queue_name)

        self.__callbacks = callbacks

        self.redirect_output()

        print(self.get_name())
        print("connected")

    def redirect_output(self):
        name = self.get_name()
        sys.stdout = StdoutRedirector(name)


    def callback(self, ch, method, properties, body):
        print("-----callback------")
        print(str(datetime.now())[:-3], end='\n')
        print(method.routing_key + ":")
        print("--------------------")
        routing_key = method.routing_key
        self.__callbacks[routing_key](body)
        ch.basic_ack(delivery_tag=method.delivery_tag, multiple=False)

    def __del__(self):
        self.__channel.close()
        self.__connection.close()

    def start(self):
        self.__channel.start_consuming()

    def _publish_message(self,message,body,exchange=constants.MAIN_EXCHANGE_NAME):
        self.__channel.basic_publish(exchange,
                                   message,
                                   body
                                     , properties=pika.BasicProperties(
                delivery_mode=2))
        print("-----publish------")
        print(str(datetime.now())[:-3], end='\n')
        print(message + ":" + body)
        print("--------------------")

    def get_name(self):
        raise NotImplementedError

    @property
    def channel(self):
        return self.__channel
