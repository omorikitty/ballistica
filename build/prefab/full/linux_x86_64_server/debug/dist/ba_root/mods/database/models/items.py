from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Inventory:
    _id: str = ""
    item: Dict[str, Dict[str, Dict | str]] = field(default_factory=dict)
