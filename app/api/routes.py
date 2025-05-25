from oxapy import Router, Status, Request  # type: ignore

from app.core.app_state import AppState
from app.api.serializers import TravelSerializer
from app.api import middleware

api = Router()
api.middleware(middleware.cache)


@api.get("/api/travel")
def get_travels(request: Request):
    app_data: AppState = request.app_data
    return app_data.travels


@api.get("/api/travel/{id}")
def retrieve_travel(request: Request, id: str):
    app_data: AppState = request.app_data
    return app_data.travels.get(id, None) or Status.NOT_FOUND


@api.post("/api/travel")
def find_bus(request: Request):
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
