from oxapy import HttpServer, Request, Cors, Router, serializer, get, post
from utils import load_bus_data, BusLine

import typing


class AppState:
    def __init__(self):
        self.buslines: typing.List[BusLine] = load_bus_data("data/travel.json")
        self.travels = [
            {"id": travel.id, "name": travel.name}
            for busline in self.buslines
            for travel in busline.travel
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
def get_travels(r: Request):
    app_data: AppState = r.app_data
    if search := r.query.get("s"):
        results = []
        for item in app_data.travels:
            if not (item in results) and (search.lower() in item["name"].lower()):
                results.append(item)
        return results
    return app_data.travels


@post("/travels")
def find_bus(r: Request):
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
            .route(get_travels)
            .scope()
            .middleware(cache_middleware)
            .route(find_bus)
        )
        .run()
    )


if __name__ == "__main__":
    main()
