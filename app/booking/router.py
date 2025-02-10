from datetime import date

from fastapi import APIRouter, Depends
from pydantic import parse_obj_as

from app.booking.dao import BookingDAO
from app.booking.schemas import BookingsInfoSchema, BookingsSchema
from app.exceptions import NoRowFindToDelete, RoomCannotBeBookedException
from app.tasks.tasks import send_bookings_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"],
)


@router.get("")
async def get_bookings(
    user: Users = Depends(get_current_user),
) -> list[BookingsInfoSchema]:
    result = await BookingDAO.find_all(user_id=user.id)
    return result


@router.post("")
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
) -> BookingsSchema:
    booked_room = await BookingDAO.add(
        user.id,
        room_id,
        date_from,
        date_to,
    )

    if booked_room is None:
        raise RoomCannotBeBookedException

    booked_room_dict = parse_obj_as(BookingsSchema, booked_room.__dict__).dict()
    send_bookings_confirmation_email.delay(
        bookings=booked_room_dict, email_to=user.email
    )

    return booked_room


@router.delete("")
async def delete_bookings(
    bookings_id: int, user: Users = Depends(get_current_user)
) -> BookingsSchema:
    deleted_booking = await BookingDAO.delete(
        id=bookings_id,
        user_id=user.id,
    )
    if not deleted_booking:
        raise NoRowFindToDelete

    return deleted_booking
