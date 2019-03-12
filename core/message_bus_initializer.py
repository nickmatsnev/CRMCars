#!/usr/bin/env python3
import pika
from lib import constants

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


channel.exchange_declare(exchange=constants.MAIN_EXCHANGE_NAME,
                         exchange_type='direct', durable=True, auto_delete=False)


channel.queue_declare(queue=constants.CLIENT_PROCESSOR_QUEUE, durable=True)

channel.queue_bind(exchange=constants.MAIN_EXCHANGE_NAME,
                   queue=constants.CLIENT_PROCESSOR_QUEUE,
                   routing_key=constants.CLIENT_RAW_CREATED_MESSAGE)

channel.queue_declare(queue=constants.SCORING_PROCESSOR_QUEUE, durable=True)

channel.queue_bind(exchange=constants.MAIN_EXCHANGE_NAME,
                   queue=constants.SCORING_PROCESSOR_QUEUE,
                   routing_key=constants.INDIVIDUAL_SCORING_PROCESS)

channel.queue_bind(exchange=constants.MAIN_EXCHANGE_NAME,
                   queue=constants.SCORING_PROCESSOR_QUEUE,
                   routing_key=constants.INDIVIDUAL_SOURCE_PROCESSED_MESSAGE)


channel.queue_bind(exchange=constants.MAIN_EXCHANGE_NAME,
                   queue=constants.SCORING_PROCESSOR_QUEUE,
                   routing_key=constants.INDIVIDUAL_PARSER_PROCESSED_MESSAGE)

channel.queue_declare(queue=constants.SOURCES_PROCESSOR_QUEUE, durable=True)

channel.queue_bind(exchange=constants.MAIN_EXCHANGE_NAME,
                   queue=constants.SOURCES_PROCESSOR_QUEUE,
                   routing_key=constants.INDIVIDUAL_SOURCE_PROCESS_MESSAGE)

channel.queue_declare(queue=constants.PARSERS_PROCESSOR_QUEUE, durable=True)

channel.queue_bind(exchange=constants.MAIN_EXCHANGE_NAME,
                   queue=constants.PARSERS_PROCESSOR_QUEUE,
                   routing_key=constants.INDIVIDUAL_PARSER_PROCESS_MESSAGE)

# channel.queue_declare(queue=constants.WILLZ_STATUS_UPDATER_QUEUE, durable=True)

# channel.queue_bind(exchange=constants.MAIN_EXCHANGE_NAME,
#                  queue=constants.WILLZ_STATUS_UPDATER_QUEUE,
#                 routing_key=constants.CLIENT_SCORING_COMPLETE_MESSAGE)

channel.close()

connection.close()


