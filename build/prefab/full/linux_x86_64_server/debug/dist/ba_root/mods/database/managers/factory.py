from database.repositories import MongoRepo
from database.managers.cache import CacheManager
from typing import Any


class ManagerFactory:
    instance: dict[str, Any] = {}
    registered: dict[str, Any] = {}

    @classmethod
    def register(cls, name: str):
        def deco(myclass):
            cls.registered[name] = {"class": myclass, "collection": name}
            print(f"Manager: {name} as been registered succesfully")
            return myclass
        return deco

    @classmethod
    def get(cls, name: str):
        if name not in cls.registered:
            raise ValueError(f"{name} is not registered")
        
        classr = cls.registered[name]
        return cls.instance.setdefault(
            name,
            classr["class"](CacheManager(name), MongoRepo(classr["collection"]))
        )