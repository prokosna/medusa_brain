import json
from enum import Enum, auto

from kafka import KafkaConsumer, TopicPartition

from ..model.image import Image


class IteratorType(Enum):
    TRIM_HORIZON = auto()
    LATEST = auto()


class Consumer:
    def __init__(self, client_id, topic, partition=0, servers=None, iter_type=IteratorType.LATEST):
        if servers is None:
            servers = ['127.0.0.1:9092']
        self.consumer = KafkaConsumer(**{'client_id': client_id, 'bootstrap_servers': servers})
        self.consumer.assign([TopicPartition(topic=topic, partition=partition)])
        if iter_type == IteratorType.TRIM_HORIZON:
            self.consumer.seek_to_beginning(TopicPartition(topic=topic, partition=partition))

    def next(self):
        msg = next(self.consumer)
        payload = json.loads(msg.value.decode('utf8'))
        return Image(**payload)

    def close(self):
        self.consumer.close()
