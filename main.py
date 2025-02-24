from oxhttp import HttpServer, Router, get, post, Response, Status
from typing import List
from models import BusLine
from json_parser import parse_bus_lines


class AppState:
    def __init__(self):
        self.buslines: List[BusLine] = parse_bus_lines("travel.json")
        self.travels = {str(travel.id): travel.name
                        for busline in self.buslines
                        for travel in busline.travel}


def get_travels(app_data: AppState):
    return Response(Status.OK(), app_data.travels)


def find_bus(travel: dict, app_data: AppState):
    primus = int(travel.get("primus"))
    terminus = int(travel.get("terminus"))

    if not primus or not terminus:
        return Response(Status.BAD_REQUEST(), {"error": "fields `primus` or `terminus` are missing"})

    bus_names = []
    for bus_line in app_data.buslines:
        primus_in_travel = any(t.id == primus for t in bus_line.travel)
        terminus_in_travel = any(t.id == terminus for t in bus_line.travel)
        if primus_in_travel and terminus_in_travel:
            bus_names.append(bus_line.name)

    return Response(Status.OK(), bus_names)


api = Router()
api.route(post("/api/travel", find_bus))
api.route(get("/api/travel", get_travels))

server = HttpServer(("0.0.0.0", 8080))
server.attach(api)
server.app_data(AppState())


if __name__ == "__main__":
    server.run()
