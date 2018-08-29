import logging
import multiprocessing
import os
import json
import argparse

import pika
import files_handler


def create_parser_for_user_arguments():
    parser = argparse.ArgumentParser(description='Start server.')
    parser.add_argument('-s', '--source', nargs='?', required=False,
                        default=os.path.join(os.path.abspath(os.getcwd()), 'source'),
                        type=str, help='Path from which server getting files for scan')
    parser.add_argument('-d', '--dist', nargs='?', required=False,
                        default=os.path.join(os.path.abspath(os.getcwd()), 'files_storage'),
                        type=str, help='Path where the server will place the downloaded files')
    parser.add_argument('-w', '--workers', nargs='?', required=False, default=5,
                        type=int, help='workers count for server')
    parser.add_argument('-r', '--rabbit', nargs='?', required=False, default='localhost',
                        type=str, help='host for RabbitMQ')
    return parser.parse_args()


class WorkerProcess(multiprocessing.Process):

    def __init__(self, **kwargs):
        multiprocessing.Process.__init__(self)
        self.dist_path = kwargs['dist_path']
        self.source_path = kwargs['source_path']
        self.rabbit_host = kwargs['rabbit_host']
        self.stop_working = multiprocessing.Event()

    def run(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.rabbit_host)
        )
        channel = connection.channel()
        channel.queue_declare(
            queue='scan_queue',
            auto_delete=False,
            durable=True
        )
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.callback, queue='scan_queue')
        channel.start_consuming()

    def callback(self, channel, method, properties, body):
        obj = json.loads(body.decode('utf-8').replace("'", '"'))
        scan_data = {
            **obj,
            'dist_path': self.dist_path,
            'source_path': self.source_path,
        }
        file_handler = files_handler.FileHandler(scan_data)
        result = file_handler.get_info()
        channel.basic_publish(exchange='',
                              routing_key=properties.reply_to,
                              properties=pika.BasicProperties(
                                  correlation_id=properties.correlation_id,
                                  delivery_mode=2,
                              ),
                              body=json.dumps(result))
        logging.info(' [.] Processed {}'.format(', '.join(obj['engines'])))
        channel.basic_ack(delivery_tag=method.delivery_tag)


def start_workers(data):
    process = WorkerProcess(**data)
    process.start()
    for i in range(data['workers']):
        process.join()


if __name__ == '__main__':
    logging.getLogger("pika").propagate = False
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    user_argument = create_parser_for_user_arguments()
    data_for_start = {
        'workers': user_argument.workers,
        'rabbit_host': user_argument.rabbit,
        'source_path': user_argument.source,
        'dist_path': user_argument.dist,
    }
    logging.info(" [x] Awaiting requests.\n"
                 " Workers count {}\n"
                 " RabbitMQ host '{}'\n"
                 " source path '{}'\n"
                 " dist path '{}'".format(
        user_argument.workers,
        user_argument.rabbit,
        user_argument.source,
        user_argument.dist,
    ))
    start_workers(data_for_start)
