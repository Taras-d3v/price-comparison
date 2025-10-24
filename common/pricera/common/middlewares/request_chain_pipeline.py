from pricera.models import ResponseObject


class RequestChainItemPipeline:
    def process_item(self, item: ResponseObject, spider):
        spider.responses[item.chain_uuid].append(item)
