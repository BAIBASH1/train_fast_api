import asyncio
from datetime import date

from fastapi import APIRouter, Request, Depends

from app.database import async_session_maker
from app.booking.dao import BookingDAO
from app.exceptions import RoomCannotBeBookedException
from app.users.models import Users
from app.users.dependencies import get_current_user
from fastapi_cache.decorator import cache


router = APIRouter(
    prefix='/bookings',
    tags=["Бронирование"],
)


@router.get("") # equal "/bookings"
async def get_bookings(user: Users = Depends(get_current_user)): #/-> list[SBookings]:
    result = await BookingDAO.find_all(user_id=user.id)
    await asyncio.sleep(2)
    return result


@router.post("/add")
async def add_booking(
        room_id: int,
        date_from: date,
        date_to: date,
        user: Users = Depends(get_current_user)
):
    booked_room = await BookingDAO.add(
        user.id,
        room_id,
        date_from,
        date_to
    )
    if not booked_room:
        raise RoomCannotBeBookedException
