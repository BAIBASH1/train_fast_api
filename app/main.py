import sys
from time import time

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.view import BookingsAdmin, HotelsAdmin, RoomsAdmin, UserAdmin
from app.booking.router import router as router_bookings
from app.database import engine
from app.hotels.rooms.router import router as router_hotels_rooms
from app.images.router import router as router_images
from app.logger import logger
from app.pages.router import router as router_page
from app.users.router import router as router_users
from config import settings

app = FastAPI()

sentry_sdk.init(
    dsn=settings.SENTRY_LINK,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
)


app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels_rooms)
app.include_router(router_page)
app.include_router(router_images)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf-8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="/cache")


@app.middleware("http")
async def record_process_time(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    logger.info(
        "Request execution time", extra={"process_time": round(time() - start_time, 3)}
    )
    return response

app = VersionedFastAPI(
    app,
    version_format="{major}",
    prefix_format="/v{major}",
    description="Greet users with a nice message",
)

app.mount(path="/static", app=StaticFiles(directory="app/static"), name="static")

instrumentor = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)

instrumentor.instrument(app).expose(app)

admin = Admin(app, engine)
admin.add_view(BookingsAdmin)
admin.add_view(UserAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
