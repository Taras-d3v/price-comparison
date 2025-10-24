import re

from bs4 import BeautifulSoup, Tag

from pricera.models.hotline.listings_model import HotlineItemOfferModel, HotlineListingsModel
import json


class HotlineListingsParser:
    base_path = "https://hotline.ua"

    @classmethod
    def parse(cls) -> None:
        return None
