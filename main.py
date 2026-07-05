from oxapy import HttpServer, Request, Cors, Router, serializer, get, post
from utils import load_bus_data, BusLine, Travel

import typing


class AppState:
    def __init__(
        self,
        bus_lines: typing.List[BusLine],
        travels: typing.List[Travel],
        travel_sets: dict,
    ) -> None:
        self.bus_lines = bus_lines
        self.travels = travels
        self.travel_sets = travel_sets
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
    app_data: AppState = r.app_data  # ty: ignore
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
        for bus_line in app_data.bus_lines
        if r.primus in app_data.travel_sets[bus_line.id]
        and r.terminus in app_data.travel_sets[bus_line.id]
    ]
    return lines


def main():
    bus_lines: typing.List[BusLine] = load_bus_data("data/travel.json")
    travels = [t for busline in bus_lines for t in busline.travel]
    travel_sets = {bl.id: {t.id for t in bl.travel} for bl in bus_lines}
    app_data = AppState(bus_lines, travels, travel_sets)
    (
        HttpServer(("0.0.0.0", 8080))
        .cors(Cors())
        .app_data(app_data)
        .attach(
            Router("/api/v1")
            .route(list_travels)
            .middleware(cache_middleware)
            .route(search_bus)
        )
        .run()
    )


if __name__ == "__main__":
    main()
