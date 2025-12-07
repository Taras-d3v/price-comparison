from pricera.common import get_mongo_client
from typing import Iterator


class BaseMongoMessageGenerator:
    def paginate(self, database: str, collection: str, filter: dict, chunk_size: int = 10_000) -> Iterator[dict]:
        with get_mongo_client() as mongo_client:
            mongo_collection = mongo_client[database][collection]

            last_id = None
            while True:
                query = filter if not last_id else filter | {"_id": {"$gt": last_id}}
                cursor = mongo_collection.find(query).sort("_id", 1).limit(chunk_size)
                documents = list(cursor)
                if not documents:
                    break
                yield from documents
                last_id = documents[-1]["_id"]
