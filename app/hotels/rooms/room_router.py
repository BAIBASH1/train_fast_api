"""
Rooms API Router.

This module defines the FastAPI router for interacting with hotel room data. It includes endpoints
for retrieving available rooms in a hotel based on specific dates. The router leverages the `RoomsDAO`
to interact with the database and return the relevant room data.

Endpoints:
    - get_hotel_rooms: Retrieves available rooms for a specified hotel and date range.
"""

from datetime import date

from app.hotels.rooms.room_dao import RoomsDAO
from app.hotels.hotel_router import router


@router.get("/{hotel_id}/rooms}")
async def get_hotel_rooms(hotel_id: int, date_from: date, date_to: date):
    """
    Asynchronously retrieves available rooms for a hotel within a specified date range.

    Args:
        hotel_id (int): The ID of the hotel to get rooms for.
        date_from (date): The start date of the booking period.
        date_to (date): The end date of the booking period.

    Returns:
        list[HotelRoomsSchema]: A list of available rooms for the given hotel and dates.
    """
    hotel_rooms_left = await RoomsDAO.get_left_rooms(
        date_from=date_from, date_to=date_to, hotel_id=hotel_id
    )
    return hotel_rooms_left
