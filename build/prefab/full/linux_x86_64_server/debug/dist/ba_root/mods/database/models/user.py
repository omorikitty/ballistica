from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class User:
    _id: str = ""
    kills: int = 0
    killed: int = 0
    score: int = 0
    coins: int = 0
    played: int = 0
    ed: str = ""
    tp: str = ""
    character: str = ""
    ls: str = ""
    name: str = ""
    accounts: List[str] = field(default_factory=list)
