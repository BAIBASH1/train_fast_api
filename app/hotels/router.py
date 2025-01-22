from datetime import date

from fastapi import APIRouter

from app.hotels.dao import HotelsDAO
from app.hotels.schemas import HotelsRoomsLeftSchema

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)


@router.get("/id/{hotel_id}")
async def get_hotel(hotel_id: int):
    hotel_inf = await HotelsDAO.find_by_id(hotel_id)
    return hotel_inf


@router.get("/{location}")
async def get_hotels_by_location_and_time(
        location: str,
        date_from: date,
        date_to: date
) -> list[HotelsRoomsLeftSchema]:
    hotels = await HotelsDAO.find_all_in_location_with_rooms_left(
        location=location,
        date_from=date_from,
        date_to=date_to,
    )
    return hotels
