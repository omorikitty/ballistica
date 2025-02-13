from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from database.settings import Config
import logging



class MongoConnect:
    def __init__(self, uri: str = Config.URI, name: str = Config.DATABASE):
        self.uri = uri or Config.DEFAULT_HOST
        self.name = name or Config.DEFAULT_DB
        self.db = None
        self.client = None

    def run(self):
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.name]
            self.client.server_info()
            print("Connect Mongodb is Succes")
        except ConnectionFailure as e:
            self.db = None
            raise RuntimeError(f"error connection to mongodb {e}")
            
            

    def __getitem__(self, collection: str):
        if self.db is None: self.run()
        return self.db[collection]

mydb = MongoConnect()