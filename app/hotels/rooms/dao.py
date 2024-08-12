from datetime import date

from sqlalchemy import select, and_, func, or_
from sqlalchemy.sql.functions import count

from app.booking.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker, engine
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.hotels.rooms.schemas import HotelRoomsSchema
from app.hotels.schemas import SHotelsRoomsLeft


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def get_left_rooms(
            cls,
            date_from: date,
            date_to: date,
            hotel_id: int
    ) -> list[HotelRoomsSchema]:

        bookings_in_dates = select(
            Bookings.room_id.label("room_id"),
            count(Bookings.id).label("non_left")
        ).where(
            and_(
                Bookings.date_from <= date_to,
                Bookings.date_to >= date_from
            )
        ).group_by(
            Bookings.room_id
        ).cte()

        hotel_rooms = select(
            Rooms.id,
            Rooms.hotel_id,
            Rooms.name,
            Rooms.description,
            Rooms.services,
            Rooms.price,
            Rooms.quantity,
            Rooms.image_id,
            ((date_to - date_from) * Rooms.price).label("total_price"),
            (Hotels.rooms_quantity - func.coalesce(bookings_in_dates.c.non_left, 0)).label("rooms_free")
        ).select_from(
            Hotels
        ).join(
            Rooms, Hotels.id == Rooms.hotel_id, isouter=True
        ).join(
            bookings_in_dates, bookings_in_dates.c.room_id == Rooms.id, isouter=True
        ).where(
            hotel_id == Hotels.id
        ).group_by(
            Rooms.id, Hotels.rooms_quantity, bookings_in_dates.c.non_left
        )

        async with async_session_maker() as session:
            print(hotel_rooms.compile(engine, compile_kwargs={"literal_binds": True}))
            res = await session.execute(hotel_rooms)
            hotel_rooms = res.mappings().all()
            return hotel_rooms
