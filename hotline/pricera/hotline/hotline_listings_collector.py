from dataclasses import dataclass
from typing import Any, Generator

from pricera.common.collectors import BaseCollector
from pricera.models import ResponseObject


@dataclass
class HotlineListingsCollector(BaseCollector):
    links: list[str]

    def crawl(self):
        from pricera.hotline.spiders.listings_spider import ListingsSpider

        return self.process_scrapy_spider(
            spider_cls=ListingsSpider, urls=self.links, proxy_config=None
        )

    def parse(self, response: ResponseObject) -> dict:
        from pricera.hotline.parsers.listings_parser import \
            HotlineListingsParser

        return HotlineListingsParser.parse(response.text)

    @classmethod
    def get_collector(cls, payload: list[str]) -> "HotlineListingsCollector":
        return cls(links=payload)


if __name__ == "__main__":
    from pricera.common import launch_collector

    launch_collector(collector_cls=HotlineListingsCollector, queue="hotline_item")
