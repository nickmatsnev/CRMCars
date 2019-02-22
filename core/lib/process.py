#!/usr/bin/env python3

from datetime import datetime
import pika

from core.lib import constants
from core.lib.global_settings import BUS_HOST
from django.core.files import File


class BasicProcess:
    __host = BUS_HOST

    def __init__(self,queue_name="",callbacks=None
                 ):
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.__host))
        self.__channel = self.__connection.channel()
        #consume not more than one message at time (between rcv & ack)
        self.__channel.basic_qos(prefetch_count=1)
        self.__channel.basic_consume(self.callback, queue_name)
        self.__callbacks = callbacks

        print("connected")

    def callback(self, ch, method, properties, body):

        print(str(datetime.now())[:-3],end='')
        routing_key = method.routing_key
        ch.basic_ack(delivery_tag=method.delivery_tag, multiple=False)

        self.__callbacks[routing_key](body)

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

    def get_name(self):
        raise NotImplementedError

    @property
    def channel(self):
        return self.__channel


