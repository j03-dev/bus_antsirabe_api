from typing import List, Dict, Set

from oxhttp import HttpServer, Response, Router, Status, get, post

from json_parser import parse_bus_lines
from models import BusLine


class AppState:
    def __init__(self):
        self.buslines: List[BusLine] = parse_bus_lines("travel.json")
        self.travels = {
            str(travel.id): travel.name
            for busline in self.buslines
            for travel in busline.travel
        }
        self.travel_sets: Dict[int, Set[int]] = {
            bus_line.id: {t.id for t in bus_line.travel}
            for bus_line in self.buslines
        }


def get_travels(app_data: AppState):
    return Response(Status.OK(), app_data.travels)


def find_bus(travel: dict, app_data: AppState):
    primus = int(travel.get("primus"))
    terminus = int(travel.get("terminus"))

    if not primus or not terminus:
        return Response(
            Status.BAD_REQUEST(),
            {
                "error": "fields `primus` or `terminus` are missing",
            },
        )

    bus_names = {
        bus_line.name
        for bus_line in app_data.buslines
        if primus in app_data.travel_sets[bus_line.id]
        and terminus in app_data.travel_sets[bus_line.id]
    }

    return Response(Status.OK(), list(bus_names))

def debug_middlware(request, next, **kwargs):
    print("body", request.json())
    return next(**kwargs)

api = Router()
api.middleware(debug_middlware)
api.route(post("/api/travel", find_bus))
api.route(get("/api/travel", get_travels))

server = HttpServer(("0.0.0.0", 8080))
server.attach(api)
server.app_data(AppState())


if __name__ == "__main__":
    server.run()
