"""
Hotels Data Access Object (DAO) for Hotel Management.

This module defines the `HotelsDAO` class, which provides asynchronous methods for interacting
with the `Hotels` model. The DAO contains functionality for querying hotels in a specific location,
finding hotels with available rooms, and retrieving detailed room availability data for a given time period.

Methods:
    - find_all_in_location_with_rooms_left: Retrieves all hotels in a location with available rooms
      within a specified date range.
"""

from datetime import date

from sqlalchemy import and_, func, select
from sqlalchemy.sql.functions import count

from app.booking.booking_models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.hotel_models import Hotels
from app.hotels.hotel_schemas import HotelsRoomsLeftSchema
from app.hotels.rooms.room_models import Rooms


class HotelsDAO(BaseDAO):
    """
    Data Access Object (DAO) for interacting with the Hotels model.

    This class provides methods to query and retrieve hotel information, including hotels in specific
    locations with available rooms and room availability for specified date ranges.
    """

    model = Hotels

    @classmethod
    async def find_all_in_location_with_rooms_left(
        cls,
        location: str,
        date_from: date,
        date_to: date,
    ) -> list[HotelsRoomsLeftSchema]:
        """
        Asynchronously retrieves all hotels in a specified location with available rooms for a given date range.

        Args:
            location (str): The location to search for hotels.
            date_from (date): The start date of the booking period.
            date_to (date): The end date of the booking period.

        Returns:
            list[HotelsRoomsLeftSchema]: A list of hotels in the specified location with available rooms.
        """
        busy_rooms = (
            select(
                Rooms.hotel_id.label("hotel_id"),
                count(Bookings.id).label("non_left"),
            )
            .select_from(Bookings)
            .join(Rooms, Rooms.id == Bookings.room_id, isouter=True)
            .where(
                and_(
                    Bookings.date_from <= date_to,
                    Bookings.date_to >= date_from,
                )
            )
            .group_by(Rooms.hotel_id)
            .cte("busy_rooms")
        )

        hotels_in_location = (
            select(
                Hotels.__table__.columns,
                (
                    Hotels.rooms_quantity
                    - func.coalesce(busy_rooms.c.non_left, 0)
                ).label("rooms_left"),
            )
            .select_from(Hotels)
            .join(busy_rooms, Hotels.id == busy_rooms.c.hotel_id, isouter=True)
            .where(
                and_(
                    Hotels.location.like(f"%{location}%"),
                    (
                        Hotels.rooms_quantity
                        - func.coalesce(busy_rooms.c.non_left, 0)
                    )
                    > 0,
                )
            )
        )

        async with async_session_maker() as session:
            hotels_rooms = await session.execute(hotels_in_location)
            hotels_rooms = hotels_rooms.mappings().all()
            return hotels_rooms
