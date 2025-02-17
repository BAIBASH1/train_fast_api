"""
Hotels Model.

This module defines the `Hotels` model, which represents hotels in the database. Each hotel
contains information such as name, location, services, room quantity, and associated rooms.
The model supports relationships with rooms and bookings.
"""

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Hotels(Base):
    """
    Hotels Model.

    This model represent hotels in the database. Each hotel contains
    information such as name, location, services, room quantity, and associated rooms. The model
    supports relationships with rooms and bookings.

    Attributes:
        - id: The unique identifier for the hotel.
        - name: The name of the hotel.
        - location: The location of the hotel.
        - services: The services provided by the hotel, stored as a JSONB object.
        - rooms_quantity: The total number of rooms in the hotel.
        - image_id: The ID of the image associated with the hotel.
        - rooms: The relationship to the `Rooms` model, representing the rooms in the hotel.
    """

    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    services: Mapped[dict] = mapped_column(JSONB)
    rooms_quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int]

    rooms: Mapped["Rooms"] = relationship(
        back_populates="hotel",
    )
