"""
Rooms Model.

This module defines the `Rooms` model, which represents rooms table in database.
Each room is associated with a specific hotel and contains information such as
room name, description, price, services, and quantity.
"""

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Rooms(Base):
    """
    Represents a hotel room in the system.

    This class defines the structure of the `rooms` table.
    Each room is associated with a specific hotel and contains information such as
    room name, description, price, services, and quantity.

    Attributes:
        - id: The unique identifier for the room.
        - hotel_id: The ID of the hotel this room belongs to.
        - name: The name of the room.
        - description: A description of the room.
        - price: The price per night for the room.
        - services: The list of services provided with the room (e.g., Wi-Fi, TV).
        - quantity: The number of available rooms.
        - image_id: The image associated with the room.
        - bookings: The relationship to the `Bookings` model.
        - hotel: The relationship to the `Hotels` model.
    """

    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(
        ForeignKey("hotels.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]
    price: Mapped[int] = mapped_column(nullable=False)
    services: Mapped[list[dict]] = mapped_column(JSON, nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int]

    bookings: Mapped["Bookings"] = relationship(
        back_populates="room",
    )

    hotel: Mapped["Hotels"] = relationship(
        back_populates="rooms",
    )
