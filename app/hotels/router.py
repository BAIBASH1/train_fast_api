from datetime import date

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.exceptions import DateToEarlierThanDateFrom, LargeIntervalBetweenDates
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import HotelsRoomsLeftSchema

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/id/{hotel_id}")
async def get_hotel(hotel_id: int):
    hotel_inf = await HotelsDAO.find_by_id(hotel_id)
    return hotel_inf


@router.get("/{location}")
@cache(expire=20)
async def get_hotels_by_location_and_time(
    location: str, date_from: date, date_to: date
) -> list[HotelsRoomsLeftSchema]:
    if date_from > date_to:
        raise DateToEarlierThanDateFrom
    if (date_to - date_from).days > 30:
        raise LargeIntervalBetweenDates

    if (date_to - date_from).days <= 30:
        hotels = await HotelsDAO.find_all_in_location_with_rooms_left(
            location=location,
            date_from=date_from,
            date_to=date_to,
        )
        return hotels
