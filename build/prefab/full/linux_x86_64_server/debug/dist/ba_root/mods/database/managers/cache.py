from time import time
from typing import Optional, Any


class CacheManager:

    def __init__(self, tag: str = "namespace") -> None:
        self.tag = tag
        self.cache = {}


    def get_from_cache(self, user: str):
        return self.cache.get(user)


    def get_cache(self) -> dict:
        return self.cache

  
    def add_to_cache(self, user: str, data: Any):
        #print(f"adding user to cache: {user}")
        self.cache[user] = data


    def update_from_cache(self, user: str, data: dict):
        if self.get_from_cache(user):
            #print(f"actualizando cache de: {user}")
            self.cache[user].update(data)


    def remove_from_cache(self, user: str):
        self.cache.pop(user, None)

    def clean(self):
        self.cache.clear()