"""
Booking Data Access Object Module

This module provides the BookingDAO class, which offers asynchronous methods
for performing booking-related operations in the database, such as adding a new
booking and retrieving all bookings for a specific user.
"""

from datetime import date

from sqlalchemy import and_, func, insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.booking.booking_models import Bookings
from app.booking.booking_schemas import BookingsInfoSchema
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.room_models import Rooms
from app.logger import logger


class BookingDAO(BaseDAO):
    """
    Data Access Object for Booking operations.

    This class provides methods to interact with the bookings in the database,
    including adding a new booking and retrieving booking information for users.
    """

    model = Bookings

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ) -> Bookings | None:
        """
        Asynchronously adds a new booking for a specified room within a given date range.

        The method checks room availability by determining the number of rooms already booked
        for the specified period and comparing it against the total quantity available.
        If at least one room is free, it retrieves the room's price, inserts a new booking
        record into the database, commits the transaction, and returns the created booking.
        In case no rooms are available or if an exception occurs during the process, it logs
        the error details and returns None.

        Args:
            user_id (int): The identifier of the user making the booking.
            room_id (int): The identifier of the room to be booked.
            date_from (date): The starting date of the booking period.
            date_to (date): The ending date of the booking period.

        Returns:
            Bookings: The newly created booking object if the booking is successful.
            None: otherwise.

        Note:
            Exceptions such as SQLAlchemyError and other general exceptions are caught and logged.
            The function does not propagate these exceptions further.
        """
        try:
            booked_rooms = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.room_id == room_id,
                        Bookings.date_from <= date_to,
                        Bookings.date_to >= date_from,
                    )
                )
                .cte("booked_rooms")
            )

            query_rooms_left = (
                select((Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left"))
                .select_from(Rooms)
                .join(
                    booked_rooms,
                    Rooms.id == booked_rooms.c.room_id,
                    isouter=True,
                )
                .where(room_id == Rooms.id)
                .group_by(Rooms.quantity, booked_rooms.c.room_id)
            )

            async with async_session_maker() as session:
                rooms_left = await session.execute(query_rooms_left)
                rooms_left: int = rooms_left.scalar()
                if rooms_left > 0:
                    query_get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(query_get_price)
                    price: int = price.scalar()
                    add_booking_query = (
                        insert(Bookings)
                        .values(
                            room_id=room_id,
                            user_id=user_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=price,
                        )
                        .returning(Bookings)
                    )
                    booking_new = await session.execute(add_booking_query)
                    await session.commit()
                    return booking_new.scalar()
                else:
                    return None
        except (SQLAlchemyError, Exception) as error:
            if isinstance(error, SQLAlchemyError):
                message = "Database Exc"
            else:
                message = "Unknown Exc"
            message += ": Cannot add booking"
            logger.error(
                "message",
                extra={
                    "user_id": user_id,
                    "room_id": room_id,
                    "date_from": date_from,
                    "date_to": date_to,
                },
                exc_info=True,
            )

    @classmethod
    async def find_all(
        cls,
        user_id: int,
    ) -> list[BookingsInfoSchema]:
        """
        Asynchronously retrieves all bookings for the specified user.

        This method queries the database to fetch booking details for the given user_id.
        It performs a join between the Bookings and Rooms tables to include related room
        information such as image, name, description, and services. The results are returned
        as a list of mappings that conform to the BookingsInfoSchema.

        Args:
            user_id (int): The identifier of the user whose bookings are to be retrieved.

        Returns:
            list[BookingsInfoSchema]: A list of booking records with associated room details.
        """
        async with async_session_maker() as session:
            query_bookings = (
                select(
                    Bookings.room_id,
                    Bookings.user_id,
                    Bookings.date_from,
                    Bookings.date_to,
                    Bookings.price,
                    Bookings.total_cost,
                    Bookings.total_days,
                    Rooms.image_id,
                    Rooms.name,
                    Rooms.description,
                    Rooms.services,
                )
                .select_from(Bookings)
                .join(Rooms, Rooms.id == Bookings.room_id, isouter=True)
                .where(user_id == Bookings.user_id)
            )
            bookings = await session.execute(query_bookings)
            bookings = bookings.mappings().all()
            return bookings
