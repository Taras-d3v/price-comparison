from pymongo import MongoClient
from dataclasses import dataclass
from pricera.message_generator.base_mongo_message_generator import BaseMongoMessageGenerator
from pricera.common import get_mongo_client, CONFIGS_DB, MESSAGE_CONFIGURATION_COLL
from enum import Enum, auto


class ConfigurationType(Enum):
    daily = auto()
    weekly = auto()


@dataclass
class MongoCollectionMessageGenerator(BaseMongoMessageGenerator):
    mongo_client: MongoClient
    configuration_type: str

    def generate_messages(self):
        message_configuration = self.mongo_client[CONFIGS_DB][MESSAGE_CONFIGURATION_COLL].find_one(
            {"configuration_type": self.configuration_type}
        )

        configurations = message_configuration["message_generator_config"]
        for config_name, config in configurations.items():
            for document in self.paginate_collection(**config):
                print(document)


if __name__ == "__main__":
    with get_mongo_client() as mongo_client:
        mongo_collection_message_generator = MongoCollectionMessageGenerator(
            mongo_client=mongo_client, configuration_type=ConfigurationType.daily.name
        )
        mongo_collection_message_generator.generate_messages()
