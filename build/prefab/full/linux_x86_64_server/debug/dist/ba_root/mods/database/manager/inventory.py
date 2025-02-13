from database.manager.cache import CacheManager
from database.models import Inventory
from database.connect import mydb
from dataclasses import asdict
from myspaz.effects import EFFECT_MAP

class InventoryPlayer:
    def __init__(self, user: str, collection: str = "customers"):
        self.cache = CacheManager(tag="customers")
        self.user = user
        self.customers = mydb[collection]
        self.effects = {}


    def inventory(self) -> dict:
        if cache:= self.cache.get_from_cache(self.user):
            return cache
        
        result = self.customers.find_one({"_id": self.user})
        if result is None:
            result = asdict(Inventory(_id = self.user))

        self.cache.add_to_cache(self.user, result)
        return result
    
    def have_item(self, name) -> bool:
        return name in self.inventory().get("item", {})

    def add_effect(self, effect: str, duration: int, **custom):
        import datetime
        expire_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=duration)
        inv = self.inventory()
        items = inv.setdefault("item", {})  
        effect_data = items.setdefault(effect, {"custom": {}, "expire": ""}) 


        effect_data["custom"].update(custom)
        effect_data["expire"] = expire_time.strftime("%d/%m/%Y, %H:%M:%S")


        self.customers.update_one({"_id": self.user}, {"$set": {"item": inv["item"]}}, upsert=True)
        self.cache.update_from_cache(self.user, inv)

        if effect in self.effects:
            self.effects[effect].update_customization(**custom)
        else:
            effect_class = EFFECT_MAP.get(effect)
            if effect_class:
                self.effects[effect] = effect_class(**custom)



    def remove_effect(self, effect: str):
        pass