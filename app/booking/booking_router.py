"""
Router module for handling booking-related API endpoints.

This module defines the FastAPI router for booking operations. It includes endpoints
to retrieve user bookings, add a new booking, and delete an existing booking. It uses
dependencies to get the current user and interacts with the `BookingDAO` class to
perform the required actions. Exceptions such as `RoomCannotBeBookedException` are raised
when necessary, and confirmation emails are sent after successfully adding a booking.
"""

from datetime import date

from fastapi import APIRouter, Depends
from pydantic import parse_obj_as

from app.booking.booking_dao import BookingDAO
from app.booking.booking_schemas import BookingsInfoSchema, BookingsSchema
from app.exceptions import NoRowFindToDelete, RoomCannotBeBookedException
from app.tasks.tasks import send_bookings_confirmation_email
from app.users.user_dependencies import get_current_user
from app.users.user_models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"],
)


@router.get("")
async def get_bookings(
    user: Users = Depends(get_current_user),
) -> list[BookingsInfoSchema]:
    """
    Retrieves all bookings for the current user.

    This endpoint fetches all bookings associated with the currently authenticated user.
    It returns a list of bookings with detailed room information such as image, name,
    description, and services.

    Args:
        user (Users): The current user, fetched using the `get_current_user` dependency.

    Returns:
        list[BookingsInfoSchema]: A list of bookings with detailed room information.
    """
    result = await BookingDAO.find_all(user_id=user.id)
    return result


@router.post("")
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
) -> BookingsSchema:
    """
    Creates a new user booking for the specified room and dates.

    This endpoint allows a user to make a booking for a specific room and date range.
    If the booking is successful, a confirmation email is sent to the user. If no rooms
    are available, a `RoomCannotBeBookedException` is raised.

    Args:
        room_id (int): The ID of the room to be booked.
        date_from (date): The start date of the booking.
        date_to (date): The end date of the booking.
        user (Users): The current user, fetched using the `get_current_user` dependency.

    Returns:
        BookingsSchema: The newly created booking object.
    """
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
    """
    Deletes an existing booking by ID.

    This endpoint allows a user to delete a specific booking. If no booking is found with
    the provided ID, a `NoRowFindToDelete` exception is raised.

    Args:
        bookings_id (int): The ID of the booking to delete.
        user (Users): The current user, fetched using the `get_current_user` dependency.

    Returns:
        BookingsSchema: The deleted booking object.
    """
    deleted_booking = await BookingDAO.delete(
        id=bookings_id,
        user_id=user.id,
    )
    if not deleted_booking:
        raise NoRowFindToDelete

    return deleted_booking
