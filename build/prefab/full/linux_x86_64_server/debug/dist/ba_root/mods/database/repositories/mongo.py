from database.connect import mydb
from pymongo import UpdateOne
from pymongo.errors import DuplicateKeyError

class MongoRepo:
    def __init__(self, collection: str) -> None:
        self.db = mydb[collection]

    def _insert(self, data: dict):
        try:
            self.db.insert_one(data)
        except DuplicateKeyError as e:
            raise e

    def save(self, user: str, data: dict):
        return self.db.update_one({"_id": user}, {"$set": data}, upsert=True)

    def _find(self, user: str):
        return self.db.find_one(user) or {}
    
    def _bulk_write(self, bulk: list[UpdateOne]):
        return self.db.bulk_write(bulk, ordered=False)
    
    def _findall(self):
        return list(self.db.find({}))