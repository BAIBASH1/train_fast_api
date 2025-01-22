from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


from app.admin.view import RoomsAdmin, BookingsAdmin, UserAdmin, HotelsAdmin
from app.database import engine
from app.pages.router import router as router_page
from app.users.router import router as router_users
from app.booking.router import router as router_bookings
from app.hotels.rooms.router import router as router_hotels_rooms
from app.images.router import router as router_images


from sqladmin import Admin


app = FastAPI()

app.mount(
    path="/static",
    app=StaticFiles(directory="app/static"),
    name="static"
)


app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels_rooms)
app.include_router(router_page)
app.include_router(router_images)

admin = Admin(app, engine)
admin.add_view(BookingsAdmin)
admin.add_view(UserAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)

# class SBooking(BaseModel):
#     room_id: int
#     date_from: date
#     date_to: date
#
#
# class SHotel(BaseModel):
#     address: str
#     name: str
#     stars: int
#
#
# class HotelsSearchArgs:
#     def __init__(
#             self,
#             location: str,
#             date_from: str,
#             date_to: str,
#             stars: Optional[int] = Query(None, ge=1, le=5),
#             has_spa: Optional[bool] = None,
#     ):
#         self.location = location
#         self.date_from = date_from
#         self.date_to = date_to
#         self.stars = stars
#         self.has_spa = has_spa
