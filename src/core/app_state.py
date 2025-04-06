from typing import List

from core.utils import BusLine, load_bus_data


class AppState:
    def __init__(self):
        self.buslines: List[BusLine] = load_bus_data("data/travel.json")
        self.travels = {
            str(travel.id): travel.name
            for busline in self.buslines
            for travel in busline.travel
        }
        self.travel_sets = {
            bus_line.id: {t.id for t in bus_line.travel} for bus_line in self.buslines
        }

        self.caches = {}
