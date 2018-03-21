import argparse
import base64
import json
from logging import getLogger, basicConfig, DEBUG, INFO

from .consuming.consumer import Consumer, IteratorType
from .event.face_detected import FaceDetected
from .messaging.publisher import Publisher
from .processing.face_detector import FaceDetector


def main(args):
    logger = getLogger(__name__)
    kafka_servers = args.kafka_servers.split(',')
    consumer = Consumer(client_id=args.id,
                        topic=args.kafka_topic,
                        servers=kafka_servers,
                        iter_type=IteratorType[args.kafka_iteration])
    detector = FaceDetector()

    while True:
        image = consumer.next()
        img = base64.b64decode(image.data)
        thumbnails = detector.detect(img)
        thumbnails = [base64.b64encode(thumbnail).decode('utf8') for thumbnail in thumbnails]
        events = []
        for thumbnail in thumbnails:
            events.append(FaceDetected(type='face_detected', timestamp=image.timestamp, thumbnail=thumbnail))
        if len(events) > 0:
            publisher = Publisher(user=args.rabbit_user,
                                  password=args.rabbit_password,
                                  host=args.rabbit_host,
                                  port=args.rabbit_port,
                                  queue=args.rabbit_queue)
            for event in events:
                publisher.publish(json.dumps(event._asdict()))
            publisher.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--id', default='brain')
    parser.add_argument('-kt', '--kafka_topic', default='test')
    parser.add_argument('-ks', '--kafka_servers', default='127.0.0.1:9092')
    parser.add_argument('-ki', '--kafka_iteration', default='LATEST')
    parser.add_argument('-ru', '--rabbit_user', default='guest')
    parser.add_argument('-rp', '--rabbit_password', default='guest')
    parser.add_argument('-rh', '--rabbit_host', default='127.0.0.1')
    parser.add_argument('-rP', '--rabbit_port', default='5672')
    parser.add_argument('-rq', '--rabbit_queue', default='medusa_brain')
    parser.add_argument('-v', '--verbose', action="store_true")
    args = parser.parse_args()
    if args.verbose:
        basicConfig(level=DEBUG)
    else:
        basicConfig(level=INFO)
    main(args)
