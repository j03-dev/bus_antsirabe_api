from oxapy import Router, Status, get, post, Request

from core.app_state import AppState
from api.serializers import TravelSerializer
from api import middleware


@get("/api/travel")
def get_travels(request: Request):
    return request.app_data.travels


@get("/api/travel/{id}")
def retrieve_travel(request: Request, id: str):
    return request.app_data.travels.get(id, None) or Status.NOT_FOUND


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


api = Router()
api.middleware(middleware.cache)
api.routes([find_bus, retrieve_travel, get_travels])
