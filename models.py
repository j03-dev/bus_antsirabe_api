from dataclasses import dataclass
from typing import List


@dataclass
class Travel:
    id: int
    name: str


@dataclass
class BusLine:
    id: int
    name: str
    primus: Travel
    termius: Travel
    travel: List[Travel]
