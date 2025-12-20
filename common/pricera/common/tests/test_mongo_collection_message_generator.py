import mongomock
import pytest
from pymongo import MongoClient
import unittest
from pricera.message_generator.mongo_collection_message_generator import (
    MongoCollectionMessageGenerator,
    ConfigurationType,
)
from pricera.message_generator.base_mongo_message_generator import BaseMongoMessageGenerator
from pricera.common import CONFIGS_DB, MESSAGE_CONFIGURATION_COLL

class TestMongoCollectionMessageGenerator(unittest.TestCase):

    def setUp(self):
        self.mongo_client = mongomock.MongoClient()
        self.message_generator = MongoCollectionMessageGenerator(
            mongo_client=self.mongo_client,
            configuration_type=ConfigurationType.daily.name
        )


    def test_generate_messages_with_filter(self):
        db = self.mongo_client[CONFIGS_DB]

        db["source_collection"].insert_many(
            [
                {"_id": 1, "value": "a", "type": "x"},
                {"_id": 2, "value": "b", "type": "y"},
                {"_id": 3, "value": "c", "type": "x"},
            ]
        )

        db[MESSAGE_CONFIGURATION_COLL].insert_one(
            {
                "configuration_type": ConfigurationType.daily.name,
                "message_generator_config": {
                    "filtered_config": {
                        "database": CONFIGS_DB,
                        "collection": "source_collection",
                        "field_mapping": [
                            {
                                "document_field_name": "value",
                                "collector_trigger_name": "bar_collector",
                                "filter": {"type": "x"},
                            }
                        ],
                    }
                },
            }
        )

        self.assertEqual(list(self.message_generator.generate_messages()), [{'bar_collector': ['a']}, {'bar_collector': ['c']}])
