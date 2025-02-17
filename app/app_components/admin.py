from sqladmin import Admin

from app.admin.view import BookingsAdmin, HotelsAdmin, RoomsAdmin, UserAdmin
from app.database import engine


def setup_admin_panel(app):
    admin = Admin(app, engine)
    admin.add_view(BookingsAdmin)
    admin.add_view(UserAdmin)
    admin.add_view(HotelsAdmin)
    admin.add_view(RoomsAdmin)
