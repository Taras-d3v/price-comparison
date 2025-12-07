from typing import Iterator
from pymongo import MongoClient
from pricera.common import ensure_list


class BaseMongoMessageGenerator:
    mongo_client: MongoClient

    def paginate_collection(self, database: str, collection: str, field_mapping: list) -> Iterator[dict]:
        for mapping in field_mapping:
            document_field_name = mapping["document_field_name"]
            collection_filter = mapping.get("filter") or {}

            projection = {document_field_name: 1, "_id": 1}

            yield from self.paginate(database, collection, collection_filter, projection)

    def paginate(
        self, database: str, collection: str, collection_filter: dict, projection: dict, chunk_size: int = 10_000
    ) -> Iterator[dict]:
        mongo_collection = self.mongo_client[database][collection]

        last_id = None
        while True:
            coll_filter = collection_filter if not last_id else collection_filter | {"_id": {"$gt": last_id}}
            cursor = mongo_collection.find(filter=coll_filter, projection=projection).sort("_id", 1).limit(chunk_size)
            documents = list(cursor)
            if not documents:
                break
            for document in documents:
                yield {k: ensure_list(v) for k, v in document.items() if k not in ["_id"]}
            last_id = documents[-1]["_id"]
