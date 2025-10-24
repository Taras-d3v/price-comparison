__all__ = [
    "RabbitMQ",
    "FileBasedMessageConsumer",
    "BaseCollector",
    "load_file_from_sub_folder",
    "get_rabbitmq_host",
    "get_rabbitmq_user",
    "get_rabbitmq_password",
]

import argparse
from dataclasses import dataclass
from typing import Callable

from .collectors import BaseCollector, FileBasedMessageConsumer, RabbitMQ
from .etl_pipeline import etl_pipeline
from .testing_utilities import load_file_from_sub_folder
from .utilities import get_rabbitmq_host, get_rabbitmq_password, get_rabbitmq_user

def get_file_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file", type=str, help="Path to the message file", required=False
    )
    args = parser.parse_args()
    return args


@dataclass
class MessageProcessor:
    collector_cls: type[BaseCollector]
    pipeline: Callable
    queue: str

    def process(self, message: dict) -> None:
        self.pipeline(
            collector_cls=self.collector_cls, message=message, queue=self.queue
        )


def launch_collector(
    collector_cls: type[BaseCollector],
    queue: str,
    pipeline: Callable = etl_pipeline,
):
    message_processor = MessageProcessor(
        collector_cls=collector_cls, pipeline=pipeline, queue=queue
    )
    args = get_file_args()
    if args.file:
        file_consumer: FileBasedMessageConsumer = FileBasedMessageConsumer(
            function=message_processor.process, file_path=args.file
        )
        file_consumer.consume()
    else:
        rabbitmq_consumer: RabbitMQ = RabbitMQ()
        rabbitmq_consumer.consume(function=message_processor.process, queue=queue)
