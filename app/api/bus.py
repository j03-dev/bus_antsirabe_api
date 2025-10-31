from oxapy import Router, Status, Request

from app.core.app_state import AppState
from app.api.serializers import TravelSerializer
from app.api import middleware

router = Router()
router.middleware(middleware.cache)


@router.get("/api/travels")
def get_travels(request: Request):
    app_data: AppState = request.app_data
    return app_data.travels


@router.get("/api/travels/{id}")
def retrieve_travel(request: Request, id: str):
    app_data: AppState = request.app_data
    return {"travel": app_data.travels.get(id, None)} or Status.NOT_FOUND


@router.post("/api/travels")
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
