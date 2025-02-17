"""
Schemas for booking data.

This module contains Pydantic schemas used for validating and serializing booking data.
The `BookingsSchema` is used for the creation and updating of bookings, while the `BookingsInfoSchema`
provides a more detailed response including room-specific information like name, description, and services.
"""

from datetime import date

from pydantic import BaseModel


class BookingsSchema(BaseModel):
    """
    Schema for representing a booking.

    This schema is used for creating and updating bookings in the system. It includes all the
    necessary fields to represent a booking, including the room, user, dates, and pricing information.
    """
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int


class BookingsInfoSchema(BaseModel):
    """
    Schema for representing detailed booking information.

    This schema is used for providing detailed information about a booking, including the room's
    image, name, description, and services, in addition to the basic booking data like dates and pricing.
    """
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int
    image_id: int
    name: str
    description: str | None
    services: list[str]
