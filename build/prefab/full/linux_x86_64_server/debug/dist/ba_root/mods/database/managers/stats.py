import datetime
from pymongo import UpdateOne
from database.models.user import User
from database.managers.factory import ManagerFactory

from dataclasses import asdict


@ManagerFactory.register("stats")
class StatsManager:
    def __init__(self, cache, repo):
        self.cache = cache
        self.stats = repo

    def get_stats(self, user: str) -> dict[str, dict]:
        cache = self.cache.get_from_cache(user)
        if cache:
            print(f"match -> {user}")
            return cache

        result = self.stats._find(user)
        if result is None:
            result = asdict(User(_id=user))

        self.cache.add_to_cache(user, result)
        return result

    def update_from_bulk(self, bulk: list[UpdateOne]):
        return self.stats._bulk_write(bulk)

    def update_stats(self, user: str, update: dict):
        result = self.stats._update(user, update)
        if result.matched_count == 0:
            return Exception(f"Failed to update stats for user: {user}")

        self.cache.add_to_cache(user, update)
