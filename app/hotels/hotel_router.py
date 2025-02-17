"""
Hotel API Router.

This module defines the FastAPI router for interacting with hotel data. It includes endpoints
for retrieving hotel information, querying hotels by location, and checking room availability.
It leverages the `HotelsDAO` class to interact with the database and return the relevant hotel data.

Endpoints:
    - get_hotel: Retrieves detailed information about a specific hotel by its ID.
    - get_hotels_by_location_and_time: Retrieves hotels in a specific location with available rooms
      for a given date range.
"""

from datetime import date

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.exceptions import DateToEarlierThanDateFrom, LargeIntervalBetweenDates
from app.hotels.hotel_schemas import HotelsRoomsLeftSchema

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/id/{hotel_id}")
async def get_hotel(hotel_id: int):
    """
    Asynchronously retrieves detailed information about a hotel by its ID.

    Args:
        hotel_id (int): The ID of the hotel to retrieve.

    Returns:
        dict: The hotel information as a dictionary.
    """
    from app.hotels.hotel_dao import HotelsDAO

    hotel_inf = await HotelsDAO.find_by_id(hotel_id)
    return hotel_inf


@router.get("/{location}")
@cache(expire=20)
async def get_hotels_by_location_and_time(
    location: str, date_from: date, date_to: date
) -> list[HotelsRoomsLeftSchema]:
    """
    Asynchronously retrieves hotels in a specified location with available rooms for a given date range.

    Args:
        location (str): The location to search for hotels.
        date_from (date): The start date of the booking period.
        date_to (date): The end date of the booking period.

    Returns:
        list[HotelsRoomsLeftSchema]: A list of hotels with available rooms in the specified location.
    """
    from app.hotels.hotel_dao import HotelsDAO

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
