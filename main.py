from oxapy import HttpServer, Request, Cors, Status, Router, serializer, get, post
from utils import load_bus_data, BusLine

import typing


class AppState:
    def __init__(self):
        self.buslines: typing.List[BusLine] = load_bus_data("data/travel.json")
        self.travels = {
            str(travel.id): travel.name
            for busline in self.buslines
            for travel in busline.travel
        }
        self.travel_sets = {
            bus_line.id: {str(t.id) for t in bus_line.travel}
            for bus_line in self.buslines
        }

        self.caches = {}


def cache(r: Request, next, **kwargs):
    app_data: AppState = r.app_data
    key = f"{r.method}/{r.uri}/{r.data}"
    if response := app_data.caches.get(key, None):
        return response
    else:
        response = next(r, **kwargs)
        app_data.caches[key] = response
        return response


class TravelSerializer(serializer.Serializer):
    primus = serializer.CharField()
    terminus = serializer.CharField()


@get("/travels")
def get_travels(request: Request):
    app_data: AppState = request.app_data
    return app_data.travels


@post("/travels")
def find_bus(request: Request):
    travel = TravelSerializer(request.data)
    travel.is_valid()
    primus = travel.validated_data["primus"]
    terminus = travel.validated_data["terminus"]

    app_data: AppState = request.app_data

    bus_names = {
        bus_line.name
        for bus_line in app_data.buslines
        if primus in app_data.travel_sets[bus_line.id]
        and terminus in app_data.travel_sets[bus_line.id]
    }

    return list(bus_names)


def main():
    (
        HttpServer(("0.0.0.0", 8080))
        .cors(Cors())
        .app_data(AppState())
        .attach(Router("/api/v1").routes([get_travels, find_bus]).middleware(cache))
        .run()
    )


if __name__ == "__main__":
    main()
