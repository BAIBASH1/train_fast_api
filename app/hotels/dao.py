from datetime import date

from sqlalchemy import select, and_, func

from app.booking.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker, engine
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(
            cls,
            location: str,
            date_from: date,
            date_to: date,
    ):
        '''
        WITH busy_rooms AS (
            SELECT hotel_id, COUNT(bookings.id) AS non_left
            FROM bookings LEFT JOIN rooms ON bookings.room_id = rooms.id
            WHERE date_from <= '2023-06-20'
              AND date_to >= '2023-05-15'
            GROUP BY hotel_id
        )
        SELECT *
        FROM hotels LEFT JOIN busy_rooms ON id = hotel_id
        WHERE location LIKE '%Алтай%'
        '''
        busy_rooms = select(
            Rooms.hotel_id, func.count(Bookings.id)
        ).join(
            Rooms, Rooms.id == Bookings.room_id, isouter=True
        ).where(and_(
            Bookings.date_from <= date_to,
            Bookings.date_to >= date_from
        )).group_by(Rooms.hotel_id)

        async with async_session_maker() as session:
            res = await session.execute(busy_rooms)
            print(13241234123)
            print(res.scalars().all())
            print(busy_rooms.compile(engine, compile_kwargs={"literal_binds": True}))
