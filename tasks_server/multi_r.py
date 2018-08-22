import multiprocessing
import pika
import json
from tasks_server import files_handler


class WorkerProcess(multiprocessing.Process):

    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.stop_working = multiprocessing.Event()

    def run(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()
        channel.queue_declare(
            queue='worker_queue',
            auto_delete=False,
            durable=True
        )
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.callback, queue='worker_queue')
        channel.start_consuming()

    def callback(self, channel, method, properties, body):
        obj = json.loads(body.decode('utf-8').replace("'", '"'))
        engines = obj.pop('engines')
        results = {}
        for engine in engines:
            scan_data = {
                'engine': engine,
                **obj
            }
            file_handler = files_handler.FileHandler(scan_data)
            result = file_handler.get_info()
            results.update({engine: {
                'result': result.get('result'),
                'error': result.get('error')}
            })
        channel.basic_publish(exchange='',
                              routing_key=properties.reply_to,
                              properties=pika.BasicProperties(
                                  correlation_id=properties.correlation_id,
                                  delivery_mode=2,
                              ),
                              body=json.dumps(results))
        channel.basic_ack(delivery_tag=method.delivery_tag)


def start_workers(num=5): #TODO make choice for workers
    for i in range(num):
        process = WorkerProcess()
        process.start()


if __name__ == '__main__':
    print(" [x] Awaiting RPC requests")
    start_workers()
