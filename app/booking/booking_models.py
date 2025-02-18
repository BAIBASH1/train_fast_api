"""
Bookings Model.

This module defines the `Bookings` class, which represents the booking records in the database.
Each booking is associated with a specific room, a user, and a booking period. The class includes
computed fields to calculate the total cost and number of days for each booking.
"""

from datetime import date

from sqlalchemy import Computed, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Bookings(Base):
    """
    Represents a booking in the system.

    This class defines the structure of the `bookings` table, which stores the information
    about each booking, including the room, user, dates, price, and the computed total cost
    and days. It also defines relationships to the `Users` and `Rooms` models.

    Attributes:
        id (int): The unique identifier for the booking.
        room_id (int): The ID of the room being booked.
        user_id (int): The ID of the user making the booking.
        date_from (date): The start date of the booking.
        date_to (date): The end date of the booking.
        price (int): The price per night for the room.
        total_cost (int): The total cost of the booking, computed as
         (date_to - date_from) * price.
        total_days (int): The total number of days for the booking, computed as
         (date_to - date_from).
        user (Users): The user who made the booking (relationship).
        room (Rooms): The room that is being booked (relationship).
    """

    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[date] = mapped_column(nullable=False)
    date_to: Mapped[date] = mapped_column(nullable=False)
    price: Mapped[int]
    total_cost: Mapped[int] = mapped_column(Computed("(date_to - date_from) * price"))
    total_days: Mapped[int] = mapped_column(Computed("(date_to - date_from)"))

    user: Mapped["Users"] = relationship(  # noqa: F821
        back_populates="bookings",
    )

    room: Mapped["Rooms"] = relationship(  # noqa: F821
        back_populates="bookings",
    )
