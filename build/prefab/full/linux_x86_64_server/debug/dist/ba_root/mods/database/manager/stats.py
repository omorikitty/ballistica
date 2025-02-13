import datetime
from pymongo import UpdateOne
from typing import Optional, List, Dict
from database.models.user import User
from database.connect import mydb
from database.manager.cache import CacheManager

from dataclasses import asdict
from typing import Any


class StatsManager:
    def __init__(self, collection: str = "stats"):
        self.cache = CacheManager(tag="stats")
        self.stats = mydb[collection]
        

    def get_stats(self, user: str) -> dict[str, Any]:
        cache = self.cache.get_from_cache(user)
        if cache:
            print(f"match -> {user}")
            return cache

        result = self.stats.find_one({"_id": user})
        if result is None:
            result = asdict(User(_id = user))

        self.cache.add_to_cache(user, result)
        return result

    def update_from_bulk(self, bulk: list[UpdateOne]):
        return self.stats.bulk_write(bulk, ordered=False)

    def update_stats(self, user: str, update: dict):
        result = self.stats.update_one({"_id": user}, {"$set": update})
        if result.matched_count == 0:
            return Exception(f"Failed to update stats for user: {user}")
        
        self.cache.add_to_cache(user, update)
