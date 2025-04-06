import json

from typing import List
from dataclasses import dataclass


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


def load_bus_data(file_path: str) -> List[BusLine]:
    with open(file_path, "r") as f:
        data = json.load(f)

    bus_lines = []
    for line in data["busLine"]:
        primus = Travel(id=line["primus"]["id"], name=line["primus"]["name"])
        termius = Travel(id=line["terminus"]["id"], name=line["terminus"]["name"])

        travels = []
        for t in line["travel"]:
            travel = Travel(id=t["id"], name=t["name"])
            travels.append(travel)

        bus_line = BusLine(
            id=line["id"],
            name=line["name"],
            primus=primus,
            termius=termius,
            travel=travels,
        )
        bus_lines.append(bus_line)

    return bus_lines
