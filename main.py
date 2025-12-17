from oxapy import HttpServer, Request, Cors, Router, serializer, get, post
from utils import load_bus_data, BusLine

import typing


class AppState:
    def __init__(self):
        self.buslines: typing.List[BusLine] = load_bus_data("data/travel.json")
        self.travels = [
            travel for busline in self.buslines for travel in busline.travel
        ]
        self.travel_sets = {
            bus_line.id: {t.id for t in bus_line.travel} for bus_line in self.buslines
        }

        self.caches = {}


class TravelSerializer(serializer.Serializer):
    primus = serializer.IntegerField()
    terminus = serializer.IntegerField()


def cache_middleware(r: Request, next, **kwargs):
    travel = TravelSerializer(r.data)
    travel.is_valid()
    primus = travel.validated_data["primus"]
    terminus = travel.validated_data["terminus"]
    key = f"{primus}/{terminus}"
    app_data: AppState = r.app_data
    if response := app_data.caches.get(key, None):
        return response
    else:
        r.primus = primus
        r.terminus = terminus
        response = next(r, **kwargs)
        app_data.caches[key] = response
        return response


@get("/travels")
def list_travels(r: Request):
    app_data: AppState = r.app_data
    if search := r.query.get("s"):
        results = []
        for travel in app_data.travels:
            if not (travel in results) and (search.lower() in travel.name.lower()):
                results.append(travel)
        return results
    return app_data.travels


@post("/travels")
def search_bus(r: Request):
    app_data: AppState = r.app_data
    lines = [
        bus_line
        for bus_line in app_data.buslines
        if r.primus in app_data.travel_sets[bus_line.id]
        and r.terminus in app_data.travel_sets[bus_line.id]
    ]
    return lines


def main():
    (
        HttpServer(("0.0.0.0", 8080))
        .cors(Cors())
        .app_data(AppState())
        .attach(
            Router("/api/v1")
            .route(list_travels)
            .scope()
            .middleware(cache_middleware)
            .route(search_bus)
        )
        .run()
    )


if __name__ == "__main__":
    main()
