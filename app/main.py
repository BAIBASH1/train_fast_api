from fastapi import FastAPI, Query, Depends
from datetime import date
import requests
from typing import Optional
from pydantic import BaseModel

from app.users.router import router as router_users
from app.booking.router import router as router_bookings
from app.hotels.router import router as router_hotels

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis


app = FastAPI()

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)


class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class SHotel(BaseModel):
    address: str
    name: str
    stars: int


class HotelsSearchArgs:
    def __init__(
            self,
            location: str,
            date_from: str,
            date_to: str,
            stars: Optional[int] = Query(None, ge=1, le=5),
            has_spa: Optional[bool] = None,
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.stars = stars
        self.has_spa = has_spa




# @app.get('/hotels')
# def get_hotels(
#         search_args: HotelsSearchArgs = Depends()
# ) -> list[SHotel]:
#     hotels = [
#         {
#             'address': 'Гагарина',
#             'name': 'Christofer',
#             'stars': 5,
#         },
#     ]
#     return hotels


@app.post('/bookings')
def add_booking(booking: SBooking):
    ...



@app.on_event("startup")
def startup():
    redis = aioredis.Redis.from_url('redis://localhost:6379', encoding='utf-8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='cache')
