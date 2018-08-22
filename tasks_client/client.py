import json
import uuid
import os

import pika

HOST = os.getenv('RABBIT_HOST', 'localhost')


class Client:

    def __init__(self):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=HOST)
        )
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True, durable=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            self.on_response,
            no_ack=False,
            queue=self.callback_queue
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, data_for_call):
        self.channel.basic_publish(exchange='',
                                   routing_key='scan_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                       delivery_mode=2,
                                   ),
                                   body=json.dumps(data_for_call))
        while self.response is None:
            self.connection.process_data_events()
        return str(self.response.decode('utf-8'))


