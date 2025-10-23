import re

from bs4 import BeautifulSoup, Tag

from pricera.models.hotline.listings_model import HotlineItemOfferModel, HotlineListingsModel
import json


class HotlineListingsParser:
    base_path = "https://hotline.ua"

    @classmethod
    def parse(cls, response_text: str) -> dict:
        soup = BeautifulSoup(response_text, "lxml")
        model = HotlineListingsModel(
            title=cls.parse_title(soup), items=cls.parse_items_list(soup)
        )
        return model.model_dump()

    @classmethod
    def parse_item(cls, item_soup: Tag) -> HotlineItemOfferModel:
        def parse_item_shop_name(item_soup: Tag) -> str:
            return item_soup.find("a", attrs={"data-eventcategory": "Pages Product Prices"}).text.strip()

        def parse_item_url(item_soup: Tag) -> str:
            item_path = item_soup.find("a", attrs={"data-eventcategory": "Pages Product Prices"})["href"]
            return cls.base_path + item_path

        def parse_item_name(item_soup: Tag) -> str:
            return item_soup.find("div", attrs={"data-eventcategory": "Pages Product Prices"}).text.strip()

        def parse_item_price(item_soup: Tag) -> float:
            return 0

        model = HotlineItemOfferModel(
            shop_name=parse_item_shop_name(item_soup),
            item_name=parse_item_name(item_soup),
            item_url=parse_item_url(item_soup),
            price=parse_item_price(item_soup),
        )

        return model

    @staticmethod
    def get_list_of_variables(script_text: str) -> dict:
        match = re.search(r'function\s*\(([^)]*)\)', script_text)
        params_str = match.group(1)
        vars_list = [v.strip() for v in params_str.split(',') if v.strip()]
        return vars_list

    @staticmethod
    def get_list_of_values(script_text: str) -> dict:
        match = re.search(r'\}\}\}\((.+)\)\);$', script_text)
        vars_str = match.group(1)

        # 1️⃣ Оборачиваем в [ ] для корректного JSON
        text = f"[{vars_str}]"
        # 2️⃣ Чиним JavaScript специфичные элементы
        text = re.sub(r'\bvoid\s*0\b', 'null', text)
        text = re.sub(r'Array\s*\(\d*\)', '[]', text)
        # 3️⃣ Парсим через json
        parsed = json.loads(text)
        return parsed

    @classmethod
    def get_variables_dict(cls, script_text: str) -> dict:
        variables = cls.get_list_of_variables(script_text)
        values = cls.get_list_of_values(script_text)
        variables_dict = dict(zip(variables, values))
        return variables_dict

    @classmethod
    def get_node_list(cls, script_text: str) -> list:
        offers_pattern = r'offers:\s*\{\s*edges:\s*\[(.*?)\]\s*,\s*currentFilters:'
        offers_match = re.search(offers_pattern, script_text, re.DOTALL)
        edges_content = offers_match.group(1)
        node_blocks = []
        node_pattern = r'\{node:\s*\{.*?\}\s*,\s*__typename:\s*\w+\}'
        nodes = re.findall(node_pattern, edges_content)
        return nodes


    @classmethod
    def parse_items_list(cls, soup: BeautifulSoup) -> list:
        script_tag = soup.find("script", text=re.compile("window.__NUXT__.+"))
        script_text = script_tag.text.strip()
        variables_dict = cls.get_variables_dict(script_text)
        node_list = cls.get_node_list(script_text)
        test = 1
        # children = product_offers.find_all("div", recursive=False)
        # product_div = children[1]
        # item_divs = product_div.find_all("div", recursive=False)
        # return list(map(cls.parse_item, item_divs))

    @staticmethod
    def parse_title(soup: BeautifulSoup) -> str:
        title_tag = soup.find("h1", class_="title__main")
        return title_tag.text.strip()
