from datetime import datetime

from app.booking.dao import BookingDAO


async def test_add_and_get_booking():
    booking = await BookingDAO.add(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime("2023-09-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-9-16", "%Y-%m-%d"),
    )

    assert booking.user_id == 2
    assert booking.room_id == 2

    booking = await BookingDAO.find_by_id(booking.id)

    assert booking is not None
