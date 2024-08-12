from datetime import date

from app.hotels.rooms.dao import RoomsDAO
from app.hotels.router import router


@router.get("/{hotel_id}/rooms}")
async def get_hotel_rooms(
        hotel_id: int,
        date_from: date,
        date_to: date
):
    hotel_rooms_left = await RoomsDAO.get_left_rooms(
        date_from=date_from,
        date_to=date_to,
        hotel_id=hotel_id
    )
    return hotel_rooms_left
