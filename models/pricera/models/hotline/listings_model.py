from pydantic import BaseModel


class HotlineItemOfferModel(BaseModel):
    shop_name: str
    item_name: str
    item_url: str
    price: float


class HotlineListingsModel(BaseModel):
    title: str
    items: list[HotlineItemOfferModel] = []
