from typing import Generator

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from pricera.common.collectors import BaseCollector


def etl_pipeline(collector_cls: BaseCollector, message: dict, queue: str) -> None:
    payload = message["payload"][queue]
    collector = collector_cls.get_collector(payload=payload)

    crawler = collector.crawl()
    responses: list = list(crawler.responses.values())

    parsed = list(map(collector.parse, responses))
    test = 1
