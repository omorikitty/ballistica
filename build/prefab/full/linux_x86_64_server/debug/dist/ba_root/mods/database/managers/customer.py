from database.managers import ManagerFactory
from database.repositories import MongoRepo
from database.managers.cache import CacheManager
from database.models import Inventory
from datetime import timedelta, datetime

from typing import Any
from dataclasses import asdict


@ManagerFactory.register("customers")
class CustomerManager:
    def __init__(self, cache: CacheManager, repo: MongoRepo):
        self.cache = cache
        self.customers = repo

    # def register(self, user: str, player):
    #     if not user in self._active_players:
    #         self._active_players[user] = player
    #         #print(f"{user} has been Registered: {self._active_players}")

    # def unregister(self, user: str):
    #     if user in self._active_players:
    #         del self._active_players[user]
    #         #print(f"borrando ref de {user}")

    def inventory(self, user: str):
        cache = self.cache.get_from_cache(user)
        # if cache:
        #     print(f"({user}) in cache return...")
        result = self.customers._find(user)
        if result: self.cache.add_to_cache(user, result)
        return cache or result
    
    def save(self, user: str, data: dict):
        self.customers.save(user, data)
    # def addEffect(self, user: str, effect: str, expire: int, **custom):
    #     expire_time = datetime.now() + timedelta(days=expire)
    #     inv = Inventory(
    #         _id = user,
    #         item = {effect: {"custom": custom, "expire": expire_time.strftime("%d/%m/%Y, %H:%M:%S")}}
    #     )
    #     inv.item["custom"].update(custom) 
    #     inv = asdict(inv)
    #     self.cache.update_from_cache(user, inv)
    #     self.customers.save(user, inv)
        
    #     player = self._active_players.get(user)

    #     if player and effect in player._active_effects:
    #         player._active_effects[effect].update_custom(**custom)
