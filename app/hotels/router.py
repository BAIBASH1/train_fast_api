from datetime import date

from fastapi import APIRouter

from app.hotels.dao import HotelsDAO

router = APIRouter(prefix="/hotels")


@router.get("/{location}")
async def get_hotels(
        location: str,
        date_from: date,
        date_to: date
):
    hotels = await HotelsDAO.find_all_in_location_with_rooms_left(
        location=location,
        date_from=date_from,
        date_to=date_to,
    )
    return hotels
