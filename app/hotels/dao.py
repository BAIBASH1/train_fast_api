from datetime import date

from sqlalchemy import select, and_, func
from sqlalchemy.sql.functions import count

from app.booking.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker, engine
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.hotels.schemas import SHotelsRoomsLeft


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all_in_location_with_rooms_left(
            cls,
            location: str,
            date_from: date,
            date_to: date,
    ) -> list[SHotelsRoomsLeft]:
        busy_rooms = select(
            Rooms.hotel_id.label('hotel_id'), count(Bookings.id).label('non_left')
        ).select_from(
            Bookings
        ).join(
            Rooms, Rooms.id == Bookings.room_id, isouter=True
        ).where(
            and_(
                Bookings.date_from <= date_to,
                Bookings.date_to >= date_from
            )
        ).group_by(
            Rooms.hotel_id
        ).cte("busy_rooms")

        hotels_in_location = select(
            Hotels.__table__.columns,
            (Hotels.rooms_quantity - func.coalesce(busy_rooms.c.non_left, 0)).label('rooms_left'),
        ).select_from(
            Hotels
        ).join(
            busy_rooms, Hotels.id == busy_rooms.c.hotel_id, isouter=True
        ).where(
            and_(
                Hotels.location.like(f'%{location}%'),
                (Hotels.rooms_quantity - func.coalesce(busy_rooms.c.non_left, 0)) > 0
            )
        )

        async with async_session_maker() as session:
            res = await session.execute(hotels_in_location)
            hotels_rooms = res.mappings().all()
            return hotels_rooms
