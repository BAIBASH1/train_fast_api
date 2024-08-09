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
    await HotelsDAO.find_all(
        location=location,
        date_from=date_from,
        date_to=date_to,
    )
    ...
