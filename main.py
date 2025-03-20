from typing import List

from oxapy import HttpServer, Router, Status, get, post, Cors, Request
from oxapy import serializer

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
def get_travels(request: Request):
    return request.app_data.travels


@get("/api/travel/{id}")
def retrieve_travel(request: Request, id: str):
    return request.app_data.travels.get(id, None) or Status.NOT_FOUND


class TravelSerializer(serializer.Serializer):
    primus = serializer.CharField()
    terminus = serializer.CharField()


@post("/api/travel")
def find_bus(request):
    travel = TravelSerializer(request)
    try:
        travel.validate()
        primus = int(travel.validate_data["primus"])
        terminus = int(travel.validate_data["terminus"])
    except Exception as e:
        return str(e), Status.BAD_REQUEST

    app_data: AppState = request.app_data

    bus_names = {
        bus_line.name
        for bus_line in app_data.buslines
        if primus in app_data.travel_sets[bus_line.id]
        and terminus in app_data.travel_sets[bus_line.id]
    }

    return list(bus_names)


def cache(request, next, **kwargs):
    app_data: AppState = request.app_data

    uri = request.uri
    method = request.method
    body = request.body

    key = f"{method}/{uri}/{body}"
    if response := app_data.caches.get(key, None):
        return response
    else:
        response = next(request, **kwargs)
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
