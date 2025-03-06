from typing import List

from oxhttp import HttpServer, Router, Status, get, post, Cors

from orjson import orjson as json
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
        self.travel_sets = {
            bus_line.id: {t.id for t in bus_line.travel} for bus_line in self.buslines
        }

        self.caches = {}


@get("/api/travel")
def get_travels(app_data: AppState):
    return json.dumps(app_data.travels).decode("utf-8")


@get("/api/travel/{id}")
def retrieve_travel(id: str, app_data: AppState):
    return json.dumps(app_data.travels.get(id, None)).decode("utf-8")\
         or Status.NOT_FOUND


@post("/api/travel", data="travel")
def find_bus(travel: dict, app_data: AppState):
    primus = int(travel.get("primus", None))
    terminus = int(travel.get("terminus", None))

    if not primus or not terminus:
        return "fields `primus` or `terminus` are missing", Status.BAD_REQUEST

    bus_names = {
        bus_line.name
        for bus_line in app_data.buslines
        if primus in app_data.travel_sets[bus_line.id]
        and terminus in app_data.travel_sets[bus_line.id]
    }

    return json.dumps(list(bus_names)).decode("utf-8")


def cache(request, next, **kwargs):
    app_data: AppState = kwargs["app_data"]

    uri = request.uri
    method = request.method
    body = request.body

    key = f"{method}/{uri}/{body}"
    if response := app_data.caches.get(key, None):
        return response
    else:
        response = next(**kwargs)
        app_data.caches[key] = response
        return response


api = Router()
api.middleware(cache)
api.routes([find_bus, retrieve_travel, get_travels])

server = HttpServer(("0.0.0.0", 8080))
server.app_data(AppState())
server.attach(api)
cors = Cors()
cors.methods = ["GET", "POST", "OPTIONS"]
server.config(cors=cors)


if __name__ == "__main__":
    server.run()
