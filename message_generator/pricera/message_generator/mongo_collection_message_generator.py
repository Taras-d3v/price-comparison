from pricera.message_generator.base_mongo_message_generator import BaseMongoMessageGenerator


class MongoCollectionMessageGenerator(BaseMongoMessageGenerator):
    def generate_messages(self):
        for document in self.paginate(database="pricera", collection="rozetka_product", filter={}):
            print(document)


if __name__ == "__main__":
    mongo_collection_message_generator = MongoCollectionMessageGenerator()
    mongo_collection_message_generator.generate_messages()
