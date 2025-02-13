from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Inventory:
    _id: str = ""
    item: Dict[str, Dict] = field(default_factory=dict)