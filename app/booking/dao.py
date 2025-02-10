from datetime import date

from sqlalchemy import and_, func, insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.booking.models import Bookings
from app.booking.schemas import BookingsInfoSchema
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from app.logger import logger


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1
              AND date_from <= '2023-06-20'
              AND date_to >=  '2023-05-15'
        SELECT (rooms.quantity - count(booked_rooms.room_id)) AS free_rooms
        FROM rooms LEFT JOIN booked_rooms
        ON rooms.id = booked_rooms.room_id
        WHERE rooms.id = 1
        GROUP BY (rooms.quantity, booked_rooms.room_id)
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
                select(
                    (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                        "rooms_left"
                    )
                )
                .select_from(Rooms)
                .join(booked_rooms, Rooms.id == booked_rooms.c.room_id, isouter=True)
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
