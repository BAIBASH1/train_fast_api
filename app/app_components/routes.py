from fastapi import FastAPI

from app.booking.booking_router import router as router_bookings
from app.hotels.rooms.room_router import router as router_hotels_rooms
from app.images.images_router import router as router_images
from app.pages.pages_router import router as router_page
from app.users.user_router import router as router_users


def include_routers(app: FastAPI):
    app.include_router(router_users)
    app.include_router(router_bookings)
    app.include_router(router_hotels_rooms)
    app.include_router(router_page)
    app.include_router(router_images)
