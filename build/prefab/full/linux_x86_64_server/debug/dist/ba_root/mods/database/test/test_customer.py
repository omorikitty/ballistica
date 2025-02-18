from database.managers import ManagerFactory
from database.models import Inventory

customers = ManagerFactory.get("customers")
user = "yei"
effect = "tag"
custom = {"tag": "hello"}
expire_time = "mytime"
inv = customers.inventory(user)

items = Inventory(_id = user, item = {effect: {"custom": custom, "expire": expire_time}})

print(items)
#print(inv)
