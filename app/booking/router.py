import asyncio
from datetime import date

from fastapi import APIRouter, Depends

from app.booking.schemas import BookingsSchema
from app.booking.dao import BookingDAO
from app.exceptions import RoomCannotBeBookedException, NoRowFindToDelete
from app.users.models import Users
from app.users.dependencies import get_current_user


router = APIRouter(
    prefix='/bookings',
    tags=["Бронирование"],
)


@router.get("")
async def get_bookings(
        user: Users = Depends(get_current_user)
) -> list[BookingsSchema]:
    result = await BookingDAO.find_all(
        user_id=user.id
    )
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
        date_to,
    )
    if not booked_room:
        raise RoomCannotBeBookedException


@router.delete("/{bookings_id}")
async def delete_bookings(
        bookings_id: int,
        user: Users = Depends(get_current_user)
):
    deleted_bookings = await BookingDAO.delete(
        id=bookings_id,
        user_id=user.id,
    )
    if not deleted_bookings:
        raise NoRowFindToDelete

    return deleted_bookings

