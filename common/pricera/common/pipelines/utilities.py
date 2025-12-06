from typing import Iterator, Tuple
import logging
from copy import deepcopy
from pricera.common import ensure_list
from pricera.common.collectors import BaseCollector

logger = logging.getLogger("pipeline_utilities")


def prepare_message(
    collector_mapping: dict[str, type[BaseCollector]], message: dict
) -> Iterator[Tuple[type[BaseCollector], dict]]:
    payload = message.get("payload")
    if not payload:
        logger.warning("Message payload is empty. Skipping pipeline processing")
        return

    for payload_key, payload_values in payload.items():
        collector_cls = collector_mapping.get(payload_key)
        if not collector_cls:
            logger.error("No collector found for payload key. Skipping.", extra={"payload_key": payload_key})
            continue

        payload_values = ensure_list(payload_values)

        # if parser/crawler supports batch: yield message without splits
        if collector_cls.supports_batch:
            batch_message = deepcopy(message)
            batch_message["payload"] = {payload_key: payload_values}
            yield collector_cls, batch_message
        # else: split message with batch payload into few messages, where each of them would have single payload
        else:
            for payload_value in payload_values:
                single_message = deepcopy(message)
                single_message["payload"] = {payload_key: payload_value}
                yield collector_cls, single_message
