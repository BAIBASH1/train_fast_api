"""
Admin Views for Managing Models in the Admin Panel.

This module defines admin views for managing the models through SQLAdmin.
The views are used to interact with the `Bookings`, `Users`, `Hotels`, and `Rooms` models
in the admin panel interface. Each view configures the columns displayed for each model.

Classes:
    - BookingsAdmin: Admin view for managing bookings.
    - UserAdmin: Admin view for managing users.
    - HotelsAdmin: Admin view for managing hotels.
    - RoomsAdmin: Admin view for managing rooms.
"""

from sqladmin import ModelView

from app.booking.booking_models import Bookings
from app.hotels.hotel_models import Hotels
from app.hotels.rooms.room_models import Rooms
from app.users.user_models import Users


class BookingsAdmin(ModelView, model=Bookings):
    """
    Admin view for managing bookings.
    """

    column_list = [c.name for c in Bookings.__table__.c]


class UserAdmin(ModelView, model=Users):
    """
    Admin view for managing users.
    """

    column_list = [Users.id, Users.email]


class HotelsAdmin(ModelView, model=Hotels):
    """
    Admin view for managing hotels.
    """

    column_list = [c.name for c in Hotels.__table__.c]


class RoomsAdmin(ModelView, model=Rooms):
    """
    Admin view for managing rooms.
    """

    column_list = [c.name for c in Rooms.__table__.c]
