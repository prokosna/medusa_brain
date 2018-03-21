from logging import getLogger

import pika

logger = getLogger(__name__)


class Publisher:
    def __init__(self, user, password, host, port, queue):
        credentials = pika.PlainCredentials(username=user, password=password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=credentials,
        ))
        self.queue = queue
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue, durable=True)

    def publish(self, msg):
        self.channel.publish(
            exchange='',
            routing_key=self.queue,
            body=msg,
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )

    def close(self):
        self.connection.close()
