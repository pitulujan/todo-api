import os
from pymongo import MongoClient

db_name = "tasks"


class MongoRepository:
    def __init__(self):
        mongo_url = os.environ.get("MONGO_URL")
        self.db = MongoClient(mongo_url)[db_name]

    def find_all(self, selector, collection_name):
        return self.db[collection_name].find(selector)

    def find_one(self, selector, collection_name):
        return self.db[collection_name].find_one(selector)

    def create(self, task, collection_name):
        return self.db[collection_name].insert_one(task)

    def update_one(self, selector, task, collection_name):
        return self.db[collection_name].update_one(selector, task).modified_count

    def delete(self, selector, collection_name):
        return self.db[collection_name].delete_one(selector).deleted_count
