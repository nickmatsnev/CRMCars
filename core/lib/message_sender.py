import pika

from core.lib import constants
from core.lib.global_settings import BUS_HOST


def send_message(message_code, body):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=BUS_HOST))
    channel = connection.channel()
    channel.basic_publish(constants.MAIN_EXCHANGE_NAME,
                          routing_key=message_code,
                          body=body, properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    connection.close()
